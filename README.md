# waybackpack `v0.6.0`

Waybackpack is a command-line tool that lets you download the entire Wayback Machine archive for a given URL.

For instance, to download every copy of the Department of Labor's homepage through 1996 (which happens to be the first year the site was archived), you'd run:

```sh
waybackpack http://www.dol.gov/ -d ~/Downloads/dol-wayback --to-date 1996
```

Result:

```sh
~/Downloads/dol-wayback/
├── 19961102145216
│   └── www.dol.gov
│       └── index.html
├── 19961103063843
│   └── www.dol.gov
│       └── index.html
├── 19961222171647
│   └── www.dol.gov
│       └── index.html
└── 19961223193614
    └── www.dol.gov
        └── index.html
```

Or, just to print the URLs of all archived snapshots:

```sh
waybackpack http://www.dol.gov/ --list
```

## Installation

```
pip install waybackpack
```

## Usage

```
usage: waybackpack [-h] [--version] (-d DIR | --list) [--raw] [--root ROOT]
                   [--from-date FROM_DATE] [--to-date TO_DATE]
                   [--user-agent USER_AGENT] [--follow-redirects]
                   [--uniques-only] [--collapse COLLAPSE] [--ignore-errors]
                   [--max-retries MAX_RETRIES] [--no-clobber] [--quiet]
                   [--progress] [--delay DELAY] [--delay-retry DELAY_RETRY]
                   url

positional arguments:
  url                   The URL of the resource you want to download.

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -d DIR, --dir DIR     Directory to save the files. Will create this
                        directory if it doesn't already exist.
  --list                Instead of downloading the files, only print the list
                        of snapshots.
  --raw                 Fetch file in its original state, without any
                        processing by the Wayback Machine or waybackpack.
  --root ROOT           The root URL from which to serve snapshotted
                        resources. Default: 'https://web.archive.org'
  --from-date FROM_DATE
                        Timestamp-string indicating the earliest snapshot to
                        download. Should take the format YYYYMMDDhhss, though
                        you can omit as many of the trailing digits as you
                        like. E.g., '201501' is valid.
  --to-date TO_DATE     Timestamp-string indicating the latest snapshot to
                        download. Should take the format YYYYMMDDhhss, though
                        you can omit as many of the trailing digits as you
                        like. E.g., '201604' is valid.
  --user-agent USER_AGENT
                        The User-Agent header to send along with your requests
                        to the Wayback Machine. If possible, please include
                        the phrase 'waybackpack' and your email address. That
                        way, if you're battering their servers, they know who
                        to contact. Default: 'waybackpack'.
  --follow-redirects    Follow redirects.
  --uniques-only        Download only the first version of duplicate files.
  --collapse COLLAPSE   An archive.org `collapse` parameter. Cf.: https://gith
                        ub.com/internetarchive/wayback/blob/master/wayback-
                        cdx-server/README.md#collapsing
  --ignore-errors       Don't crash on non-HTTP errors e.g., the requests
                        library's ChunkedEncodingError. Instead, log error and
                        continue. Cf.
                        https://github.com/jsvine/waybackpack/issues/19
  --max-retries MAX_RETRIES
                        How many times to try accessing content with 4XX or
                        5XX status code before skipping?
  --no-clobber          If a file is already present (and >0 filesize), don't
                        download it again.
  --quiet               Don't log progress to stderr.
  --progress            Print a progress bar. Mutes the default logging.
                        Requires `tqdm` to be installed.
  --delay DELAY         Sleep X seconds between each fetch.
  --delay-retry DELAY_RETRY
                        Sleep X seconds between each post-error retry.
```

## Support

Waypackback is written in pure Python, depends only on [`requests`](docs.python-requests.org), and should work wherever Python works. Should be compatible with both Python 2 and Python 3.

## Thanks

Many thanks to the following users for catching bugs, fixing typos, and proposing useful features:

- [@grawity](https://github.com/grawity)
- [@taggartk](https://github.com/taggartk)
- [@jtemplon](https://github.com/jtemplon)
- [@jwilk](https://github.com/jwilk)
- [@wumpus](https://github.com/wumpus)
- [@bevacqua](https://github.com/bevacqua)
- [@ErikBorra](https://github.com/ErikBorra)
- [@StevenACoffman](https://github.com/StevenACoffman)
- [@Hunter-Github](https://github.com/Hunter-Github)
- [@jeremybmerrill](https://github.com/jeremybmerrill)
- [@peci1](https://github.com/peci1)
- [@shijialee](https://github.com/shijialee)
- [@pmlandwehr](https://github.com/pmlandwehr)
