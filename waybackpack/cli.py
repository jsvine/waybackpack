#!/usr/bin/env python
from .archive import Resource, DEFAULT_ROOT
import argparse
import logging

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("url",
        help="The URL of the resource you want to download.")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-d", "--dir",
        help="Directory to save the files.")

    group.add_argument("--list",
        action="store_true",
        help="Instead of downloading the files, only print the list of snapshots.")

    parser.add_argument("--original",
        action="store_true",
        help="Fetch file in its original state, without snappshotted images/CSS/JS.")

    parser.add_argument("--root", default=DEFAULT_ROOT,
        help="The root URL from which to serve snapshotted resources. Default: '{0}'".format(DEFAULT_ROOT))

    parser.add_argument("--prefix",
        help="Prefix to prepend to saved files. Defaults to the URL, with all non-alphanumeric characters replaced with hyphens.")

    parser.add_argument("--suffix",
        help="Suffix to append to saved files. Defaults to the file extension of the URL you're downloading.")

    parser.add_argument("--start",
        help="Timestamp-string indicating the earliest snapshot to download. Should take the format YYYYMMDDhhss, though you can omit as many of the trailing digits as you like. E.g., '201501' is valid.")

    parser.add_argument("--end",
        help="Timestamp-string indicating the latest snapshot to download. Should take the format YYYYMMDDhhss, though you can omit as many of the trailing digits as you like. E.g., '201604' is valid.")

    parser.add_argument("--quiet",
        action="store_true",
        help="Don't log progress to stderr.")

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    
    logging.basicConfig(level=(logging.WARN if args.quiet else logging.INFO))

    resource = Resource(args.url)
    if args.start != None or args.end != None:
        resource = resource.between(args.start, args.end)

    if args.dir:
        resource.download_to(args.dir,
            original=args.original,
            root=args.root,
            prefix=args.prefix,
            suffix=args.suffix)
    else:
        flag = "id_" if args.original else ""
        urls = (s.get_url(flag) for s in resource.snapshots)
        print("\n".join(urls))

if __name__ == "__main__":
    main()
