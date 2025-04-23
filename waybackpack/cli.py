#!/usr/bin/env python
import argparse
import logging

from .cdx import search
from .pack import Pack
from .session import Session
from .settings import DEFAULT_ROOT, DEFAULT_USER_AGENT
from .version import __version__


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )

    parser.add_argument("url", help="The URL of the resource you want to download.")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-d",
        "--dir",
        help="Directory to save the files. Will create this directory if it doesn't already exist.",
    )

    group.add_argument(
        "--list",
        action="store_true",
        help="Instead of downloading the files, only print the list of snapshots.",
    )

    parser.add_argument(
        "--raw",
        action="store_true",
        help="Fetch file in its original state, without any processing by the Wayback Machine or waybackpack.",
    )

    parser.add_argument(
        "--root",
        default=DEFAULT_ROOT,
        help="The root URL from which to serve snapshotted resources. Default: '{0}'".format(
            DEFAULT_ROOT
        ),
    )

    parser.add_argument(
        "--from-date",
        help="Timestamp-string indicating the earliest snapshot to download. Should take the format YYYYMMDDhhss, though you can omit as many of the trailing digits as you like. E.g., '201501' is valid.",
    )

    parser.add_argument(
        "--to-date",
        help="Timestamp-string indicating the latest snapshot to download. Should take the format YYYYMMDDhhss, though you can omit as many of the trailing digits as you like. E.g., '201604' is valid.",
    )

    parser.add_argument(
        "--user-agent",
        help="The User-Agent header to send along with your requests to the Wayback Machine. If possible, please include the phrase 'waybackpack' and your email address. That way, if you're battering their servers, they know who to contact. Default: '{0}'.".format(
            DEFAULT_USER_AGENT
        ),
        default=DEFAULT_USER_AGENT,
    )

    parser.add_argument(
        "--follow-redirects", help="Follow redirects.", action="store_true"
    )

    parser.add_argument(
        "--uniques-only",
        help="Download only the first version of duplicate files.",
        action="store_true",
    )

    parser.add_argument(
        "--collapse",
        help="An archive.org `collapse` parameter. E.g., --collapse timestamp:6 collapses results to at most one per month. See here: https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md#collapsing",
        action="append",
    )

    parser.add_argument(
        "--ignore-errors",
        help="Don't crash on non-HTTP errors e.g., the requests library's ChunkedEncodingError. Instead, log error and continue. See here: https://github.com/jsvine/waybackpack/issues/19",
        action="store_true",
    )

    parser.add_argument(
        "--max-retries",
        help="How many times to try accessing content with 4XX or 5XX status code before skipping?",
        type=int,
        default=3,
    )

    parser.add_argument(
        "--no-clobber",
        action="store_true",
        help="If a file is already present (and >0 filesize), don't download it again.",
    )

    parser.add_argument(
        "--quiet", action="store_true", help="Don't log progress to stderr."
    )

    parser.add_argument(
        "--progress",
        action="store_true",
        help="Print a progress bar. Mutes the default logging. Requires `tqdm` to be installed.",
    )

    parser.add_argument(
        "--delay", type=int, default=0, help="Sleep X seconds between each fetch."
    )

    parser.add_argument(
        "--delay-retry",
        type=int,
        default=5,
        help="Sleep X seconds between each post-error retry.",
    )

    parser.add_argument(
        "--proxy",
        default=None,
        help="Use a proxy to connect to the archive.org"
    )

    parser.add_argument(
        "--no-verify-certificate",
        action='store_false',
        default=True,
        help="Don`t verify the certificate of archive.org"
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    logging.basicConfig(
        level=(logging.WARN if (args.quiet or args.progress) else logging.INFO),
        format="%(levelname)s:%(name)s: %(message)s",
    )

    session = Session(
        user_agent=args.user_agent,
        follow_redirects=args.follow_redirects,
        max_retries=args.max_retries,
        delay_retry=args.delay_retry,
        proxy=args.proxy,
        verify=args.no_verify_certificate
    )

    snapshots = search(
        args.url,
        session=session,
        from_date=args.from_date,
        to_date=args.to_date,
        uniques_only=args.uniques_only,
        collapse=args.collapse,
    )

    timestamps = [snap["timestamp"] for snap in snapshots]

    pack = Pack(args.url, timestamps=timestamps, session=session)

    if args.dir:
        pack.download_to(
            args.dir,
            raw=args.raw,
            root=args.root,
            ignore_errors=args.ignore_errors,
            no_clobber=args.no_clobber,
            progress=args.progress,
            delay=args.delay,
        )
    else:
        flag = "id_" if args.raw else ""
        urls = (a.get_archive_url(flag) for a in pack.assets)
        print("\n".join(urls))


if __name__ == "__main__":
    main()
