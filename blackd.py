import asyncio
import logging

from aiohttp import web
import black
import click

# This is used internally by tests to shut down the server prematurely
_stop_signal = asyncio.Event()

VERSION_HEADER = "X-Protocol-Version"
LINE_LENGTH_HEADER = "X-Line-Length"
PYTHON_VARIANT_HEADER = "X-Python-Variant"
SKIP_STRING_NORMALIZATION_HEADER = "X-Skip-String-Normalization"
FAST_OR_SAFE_HEADER = "X-Fast-Or-Safe"


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--bind-host", type=str, help="Address to bind the server to.", default="localhost"
)
@click.option("--bind-port", type=int, help="Port to listen on", default=45484)
@click.version_option(version=black.__version__)
def main(bind_host: str, bind_port: int) -> None:
    logging.basicConfig(level=logging.INFO)
    app = make_app()
    ver = black.__version__
    black.out(f"blackd version {ver} listening on {bind_host} port {bind_port}")
    web.run_app(app, host=bind_host, port=bind_port, handle_signals=True, print=None)


def make_app() -> web.Application:
    app = web.Application()
    app.add_routes([web.post("/", handle)])
    return app


async def handle(request: web.Request) -> web.Response:
    try:
        if request.headers.get(VERSION_HEADER, "1") != "1":
            return web.Response(
                status=501, text="This server only supports protocol version 1"
            )
        try:
            line_length = int(
                request.headers.get(LINE_LENGTH_HEADER, black.DEFAULT_LINE_LENGTH)
            )
        except ValueError:
            return web.Response(status=400, text="Invalid line length header value")
        py36 = False
        pyi = False
        if PYTHON_VARIANT_HEADER in request.headers:
            value = request.headers[PYTHON_VARIANT_HEADER]
            if value == "pyi":
                pyi = True
            else:
                try:
                    major, *rest = value.split(".")
                    if int(major) == 3 and len(rest) > 0:
                        if int(rest[0]) >= 6:
                            py36 = True
                except ValueError:
                    return web.Response(
                        status=400, text=f"Invalid value for {PYTHON_VARIANT_HEADER}"
                    )
        skip_string_normalization = bool(
            request.headers.get(SKIP_STRING_NORMALIZATION_HEADER, False)
        )
        fast = False
        if request.headers.get(FAST_OR_SAFE_HEADER, "safe") == "fast":
            fast = True
        mode = black.FileMode.from_configuration(
            py36=py36, pyi=pyi, skip_string_normalization=skip_string_normalization
        )
        req_bytes = await request.content.read()
        charset = request.charset if request.charset is not None else "utf8"
        req_str = req_bytes.decode(charset)
        formatted = black.format_file_contents(
            req_str, line_length=line_length, fast=fast, mode=mode
        ).encode(charset)
        return web.Response(
            content_type=request.content_type, charset=charset, body=formatted
        )
    except black.NothingChanged:
        return web.Response(status=204)
    except Exception as e:
        logging.exception("Exception during handling a request")
        return web.Response(status=500, text=str(e))


if __name__ == "__main__":
    black.patch_click()
    main()
