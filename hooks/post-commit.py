#!/usr/bin/env python

from __future__ import unicode_literals, print_function

import os, sys, subprocess, logging

logging.basicConfig(level=logging.DEBUG)

from _hook_config import SHARED_AUTOMERGE_SUFFIX, POST_COMMIT_REMOTES_TO_UPDATE


def branch_mapper(remote, local_branch):
    if remote not in POST_COMMIT_REMOTES_TO_UPDATE:
        return None
    return local_branch + SHARED_AUTOMERGE_SUFFIX

BRANCH_MAPPING = branch_mapper


def get_checked_out_branch():
    """
    :return: String with currently checked out branch
    """
    return subprocess.check_output("git rev-parse --symbolic-full-name --abbrev-ref HEAD".split()).strip()


def get_list_of_remotes():
    return map(str.strip, subprocess.check_output("git remote".split()).split())


def main():

    logging.debug("Config: SHARED_AUTOMERGE_SUFFIX:%s", SHARED_AUTOMERGE_SUFFIX)
    logging.debug("Config: POST_COMMIT_REMOTES_TO_UPDATE:%s", POST_COMMIT_REMOTES_TO_UPDATE)

    current_branch = get_checked_out_branch()
    remotes = get_list_of_remotes()

    logging.debug("Remotes %s", remotes)

    for r in remotes:
        push_to_branch = BRANCH_MAPPING(r, current_branch)
        logging.debug("%s", (current_branch, r, push_to_branch))
        if push_to_branch is None:
            continue
        subprocess.check_call(['git', 'push', r, '{}:{}'.format(current_branch,push_to_branch)])

if __name__ == "__main__":
    main()
