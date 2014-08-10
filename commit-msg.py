#!/usr/bin/env python

from __future__ import unicode_literals, print_function

import os, sys, subprocess, logging

logging.basicConfig(level=logging.INFO)

REMOTES_TO_UPDATE = ['cis']

LOCAL_BRANCHES_TO_PUSH = ['dev', 'master']

AUTOMERGE_SUFFIX = "-automerge"


def branch_mapper(remote, local_branch):
    if remote not in REMOTES_TO_UPDATE:
        return None
    if local_branch not in LOCAL_BRANCHES_TO_PUSH:
        return None
    return local_branch + AUTOMERGE_SUFFIX

BRANCH_MAPPING = branch_mapper


def get_checked_out_branch():
    """
    :return: String with currently checked out branch
    """
    return subprocess.check_output("git rev-parse --symbolic-full-name --abbrev-ref HEAD".split()).strip()


def get_list_of_remotes():
    return map(str.strip, subprocess.check_output("git remote".split()).split())


def main():

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
