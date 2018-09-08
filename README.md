# White

  
<h2 align="center">A Fork of Black with nicer, more idiomatic defaults</h2>

White is a fork of Black with the following differences:

- White doesn't downgrade strings to double quotes.
- (WIP) White doesn't go overboard with separate indented lines.
- White uses 120 line length instead of 88, which is sensible 
  since computer screens are larger now then were 
  when 88 was popularized. 

### Installation

*White* can be installed by running `pip install git+https://github.com/iMerica/white.git@master`.  It requires
Python 3.6.0+ to run but you can reformat Python 2 code with it, too.


### Usage

To get started right away with sensible defaults:

```
white {source_file_or_directory}
```

### Command line options

*White* doesn't provide many options.  You can list them by running
`white --help`:

```text
white [OPTIONS] [SRC]...

Options:
  -l, --line-length INTEGER   Where to wrap around.  [default: 88]
  --py36                      Allow using Python 3.6-only syntax on all input
                              files.  This will put trailing commas in function
                              signatures and calls also after *args and
                              **kwargs.  [default: per-file auto-detection]
  --pyi                       Format all input files like typing stubs
                              regardless of file extension (useful when piping
                              source on standard input).
                              Don't normalize string quotes or prefixes.
  --check                     Don't write the files back, just return the
                              status.  Return code 0 means nothing would
                              change.  Return code 1 means some files would be
                              reformatted.  Return code 123 means there was an
                              internal error.
  --diff                      Don't write the files back, just output a diff
                              for each file on stdout.
  --fast / --safe             If --fast given, skip temporary sanity checks.
                              [default: --safe]
  --include TEXT              A regular expression that matches files and
                              directories that should be included on
                              recursive searches. On Windows, use forward
                              slashes for directories.  [default: \.pyi?$]
  --exclude TEXT              A regular expression that matches files and
                              directories that should be excluded on
                              recursive searches. On Windows, use forward
                              slashes for directories.  [default:
                              build/|buck-out/|dist/|_build/|\.git/|\.hg/|
                              \.mypy_cache/|\.tox/|\.venv/]
  -q, --quiet                 Don't emit non-error messages to stderr. Errors
                              are still emitted, silence those with
                              2>/dev/null.
  -v, --verbose               Also emit messages to stderr about files
                              that were not changed or were ignored due to
                              --exclude=.
  --version                   Show the version and exit.
  --config PATH               Read configuration from PATH.
  --help                      Show this message and exit.
```
