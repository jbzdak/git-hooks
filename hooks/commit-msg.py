#!/usr/bin/env python

from __future__ import unicode_literals, print_function

import os, sys, logging, re, codecs

logging.basicConfig(level=logging.ERROR)

from _hook_config import COMMIT_MSG_MIN_LENGTH, COMMIT_MSG_REQUIRED_REGEXPS


def main():
    file_path = sys.argv[1]
    with codecs.open(file_path, encoding="utf-8") as f:
        lines = map(lambda x: x.strip(), f)
        non_comment_lines = filter(lambda x: x and x[0] != '#', lines)
        commit = "".join(non_comment_lines)
        if COMMIT_MSG_MIN_LENGTH and COMMIT_MSG_MIN_LENGTH > 0 and len(commit) < COMMIT_MSG_MIN_LENGTH:
            logging.error("Commit message to short")
            sys.exit(1)
        if COMMIT_MSG_REQUIRED_REGEXPS:
            for regexp in COMMIT_MSG_REQUIRED_REGEXPS:
                if not re.findall(regexp, commit):
                    logging.error("Commit should contain pattern %s", regexp)
                    sys.exit(1)


if __name__ == "__main__":
    main()