#!/usr/bin/env python

from __future__ import unicode_literals, print_function

import os, sys, logging, re, codecs

logging.basicConfig(level=logging.ERROR)

MIN_COMMIT_LENGTH = 15

REQUIRED_REGEXPS = [
    'KK-\d+'
]

def main():
    file_path = sys.argv[1]
    with codecs.open(file_path, encoding="utf-8") as f:
        lines = map(lambda x: x.strip(), f)
        non_comment_lines = filter(lambda x: x and x[0] != '#', lines)
        commit = "".join(non_comment_lines)
        if MIN_COMMIT_LENGTH and len(commit) < MIN_COMMIT_LENGTH:
            logging.error("Commit message to short")
            sys.exit(1)
        if REQUIRED_REGEXPS:
            for regexp in REQUIRED_REGEXPS:
                if not re.findall(regexp, commit):
                    logging.error("Commit should contain pattern %s", regexp)
                    sys.exit(1)


if __name__ == "__main__":
    main()