#!/usr/bin/env python3

from __future__ import unicode_literals, print_function

import os, sys, logging, re, codecs
import subprocess

logging.basicConfig(level=logging.INFO)

from _hook_config import PRE_COMMMIT_FORBIDDEN_BRANCHES


def get_checked_out_branch():
    """
    :return: String with currently checked out branch
    """
    return subprocess.check_output("git rev-parse --symbolic-full-name --abbrev-ref HEAD".split()).strip().decode('utf-8')


def main():
    current_branch = get_checked_out_branch()
    logging.debug("Current branch %s forbidding to %s", current_branch, PRE_COMMMIT_FORBIDDEN_BRANCHES)
    if current_branch in PRE_COMMMIT_FORBIDDEN_BRANCHES:
        logging.info("Forbidding commit to {}".format(current_branch))
        sys.exit(1)


if __name__ == "__main__":
    main()