#!/usr/bin/env python

from __future__ import unicode_literals, print_function

import os, sys, logging, re, codecs
import subprocess

logging.basicConfig(level=logging.DEBUG)

from _hook_config import PRE_COMMMIT_FORBIDDEN_BRANCHES


def get_checked_out_branch():
    """
    :return: String with currently checked out branch
    """
    return subprocess.check_output("git rev-parse --symbolic-full-name --abbrev-ref HEAD".split()).strip()


def main():
    current_branch = get_checked_out_branch()
    if current_branch in PRE_COMMMIT_FORBIDDEN_BRANCHES:
        logging.info("Forbidding commit to {}".format(current_branch))


if __name__ == "__main__":
    main()