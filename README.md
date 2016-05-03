# waybackpack

Waybackpack is a command-line tool that lets you download the entire Wayback Machine archive for a given URL.

For instance, to download every copy of the Department of Labor's homepage before 1997, you'd run:

```sh
# Create a directory where you'll store the saved pages.
mkdir ~/Downloads/dol-dot-gov

# Download all the dol.gov copies to that directory
waybackpack dol.gov -d ~/Downloads/dol-dot-gov --end 1997
```

Or, just to print the URLs of all archived snapshots:

```sh
waybackpack dol.gov --list
```

## Installation

```
pip install waybackpack
```

## Usage

```
waybackpack [-h] (-d DIR | --list) [--original] [--root ROOT]
              [--prefix PREFIX] [--suffix SUFFIX] [--start START] [--end END]
              [--user-agent USER_AGENT] [--quiet]
              url

positional arguments:
  url                   The URL of the resource you want to download.

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Directory to save the files.
  --list                Instead of downloading the files, only print the list
                        of snapshots.
  --original            Fetch file in its original state, without snapshotted
                        images/CSS/JS.
  --root ROOT           The root URL from which to serve snapshotted
                        resources. Default: 'https://web.archive.org'
  --prefix PREFIX       Prefix to prepend to saved files. Defaults to the URL,
                        with all non-alphanumeric characters replaced with
                        hyphens.
  --suffix SUFFIX       Suffix to append to saved files. Defaults to the file
                        extension of the URL you're downloading.
  --start START         Timestamp-string indicating the earliest snapshot to
                        download. Should take the format YYYYMMDDhhss, though
                        you can omit as many of the trailing digits as you
                        like. E.g., '201501' is valid.
  --end END             Timestamp-string indicating the latest snapshot to
                        download. Should take the format YYYYMMDDhhss, though
                        you can omit as many of the trailing digits as you
                        like. E.g., '201604' is valid.
  --user-agent USER_AGENT
                        The User-Agent header to send along with your requests
                        to the Wayback Machine. If possible, please include
                        the phrase 'waybackpack' and your email address. That
                        way, if you're battering their servers, they know who
                        to contact. Default: 'waybackpack'.
  --quiet               Don't log progress to stderr.
```

## Support

Waypackback is written in dependency-less Python, and should work wherever Python works. Should be compatible with both Python 2 and Python 3.

## Thanks

Many thanks to the following users for catching bugs and/or proposing fixes:

- [@grawity](https://github.com/grawity)
- [@taggartk](https://github.com/taggartk)
- [@jtemplon](https://github.com/jtemplon)
