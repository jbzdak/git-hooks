#!/usr/bin/env python 
"""

Description
-----------

Update hook that automatically merges changes inside the repository.
It's creation was sparked by
`my question on SO <http://stackoverflow.com/q/25207942/7918>`_.
Especially by `this answer <http://stackoverflow.com/a/25209198/7918>`_.

Logic is as follows:
--------------------

If repository recleives a push we will merge pushed branch to curren branch if
following conditions are met:

* This repo is not bare. It is bare **push will fail**
* pushed branch has a special suffix (by default ``-automerge``). If
 pushed branch has no suffix push will not be aborted.
* Currently checked out branch is named as branch we push to without suffix.
 so if push was to ``foo-automerge``, we will merge iff checked out branch
 is ``foo``. If other branch is checked out push will not be aborted.
* Working directory is clean. If working directory is dirty (and previous
 condition are met) **push will fail**.
* We can guess working copy directory. If not can't  **push will fail**.
* Merge is fast-forward if not **push will fail**.

Installation:
-------------

Copy this file to .git/hooks, and link it to **both**, ``update``
and ``pre-update``. You need to add it to both hooks because ``pre-update`` is
needed to fail push when error conditions are met, and ``update`` is needed
to actually do merge.

Add executable permissions to both hooks.



"""
from __future__ import unicode_literals, print_function

import os, sys, subprocess, logging

logging.basicConfig(level=logging.INFO)
"""
Set do ``DEBUG`` for debug info, or to ``ERROR`` to get error conditions only.
"""

from _hook_config import (
    SHARED_AUTOMERGE_SUFFIX, UPDATE_CAN_GUESS_GIT_WORK_TREE,
    UPDATE_FORCE_WORKING_DIR
)


def get_working_copy_dir():
    """
    Tries to guess and returns working copy directory.
    """

    if UPDATE_FORCE_WORKING_DIR:
        return UPDATE_FORCE_WORKING_DIR

    working_copy = os.environ.get("GIT_WORK_TREE", None)
    if working_copy is not None:
        return working_copy
    if not UPDATE_CAN_GUESS_GIT_WORK_TREE:
        logging.error("Can't quess working copy dir and 'GIT_WORK_TREE' was "
                      "not set")
        sys.exit(1)
    path = os.path.abspath(os.environ['GIT_DIR'])
    working_copy, git_dir = os.path.split(path)
    git_dir = git_dir.strip()
    if git_dir != ".git":
        logging.error("Can't guess working copy dir, because GIT_DIR does not "
                      "point to directory named '.git'")
        sys.exit(1)
    return working_copy


def strip_branch(branch):
    """
    Removes git decorations from branch name.

    >>> strip_branch("refs/heads/feature/master-automerge")
    'feature/master-automerge'
    >>> strip_branch("refs/heads/master-automerge")
    'master-automerge'
    >>> strip_branch('refs/heads/master-automerge ')
    'master-automerge'
    """
    return "/".join(branch.split("/")[2:]).strip()


def checked_out_branch_is_valid(pushed_branch):
    """
    Check whether checked out branch mathes branch we are pushing to.

    """
    pushed_branch_sans_automerge = pushed_branch[:-len(SHARED_AUTOMERGE_SUFFIX)]
    checked_out_branch = get_checked_out_branch()

    if checked_out_branch != pushed_branch_sans_automerge:
        logging.info("Other branch is checked out, will not merge working copy")
        sys.exit(0)


def is_this_repo_bare():
    """
    :return: True if this repository is bare, False otherwise.
    """
    result = subprocess.check_output("git rev-parse --is-bare-repository".split()).strip()
    if result == "true":
        return True
    if result == "false":
        return False
    raise ValueError("Can't guess whether this repository is bare {}".format(result))


def git_subprocess(args):
    """
    Utility function to call git process in the working copy directory.
    :param list args: list of string containing command to call
    """
    new_cwd = get_working_copy_dir()
    logging.debug("Working copy dir %s", new_cwd)

    new_env = dict(os.environ)
    new_env["GIT_DIR"] = os.path.abspath(os.environ['GIT_DIR'])
    return subprocess.check_output(args, cwd=new_cwd, env=new_env)


def get_checked_out_branch():
    """
    :return: String with currently checked out branch
    """
    return git_subprocess("git rev-parse --symbolic-full-name --abbrev-ref HEAD".split()).strip()


def check_working_directory_clean():
    """
    This is adapted from here: http://stackoverflow.com/a/3879077/7918

    Will exit id working copy is dirty.
    """
    try:
        # Update the index
        git_subprocess("git update-index -q --ignore-submodules --refresh".split())
        # Disallow unstaged changes in the working tree
        git_subprocess("git diff-files --quiet --ignore-submodules --".split())
        # Disallow uncommitted changes in the index
        git_subprocess("git diff-index --cached --quiet HEAD --ignore-submodules --".split())
    except subprocess.CalledProcessError:
        logging.error("Working directory here is not clean. Will not merge")
        sys.exit(1)


def validate(pushed_branch):

    """
    If we can't merge ``pushed_branch`` to current branch this function will
    print error and call ``sys.exit`` with apropriate exit code.
    """

    if is_this_repo_bare():
        logging.error("Sorry this hook will not work on bare repository")
        sys.exit(1)

    logging.debug("Updating branch %s", pushed_branch)
    if not pushed_branch.endswith(SHARED_AUTOMERGE_SUFFIX):
        logging.debug("Branch has no automerge suffix, will not automatically merge")
        sys.exit(0)

    checked_out_branch_is_valid(pushed_branch)

    check_working_directory_clean()

    logging.debug("OK to merge")


def update_hook(pushed_branch):

    validate(pushed_branch)


def post_update_hook(pushed_branch):

    validate(pushed_branch)

    try:
        git_subprocess(['git', 'merge', '--ff-only', pushed_branch])
    except subprocess.CalledProcessError:
        logging.error("Couldn't merge --- merge was not fast forward")
        sys.exit(1)


def main():

    script_name = sys.argv[0]
    pushed_branch = sys.argv[1]

    pushed_branch = strip_branch(pushed_branch)

    if script_name.endswith('/update'):
        update_hook(pushed_branch)
    if script_name.endswith('/post-update'):

        post_update_hook(pushed_branch)

if __name__ == "__main__":
    main()