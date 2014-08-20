#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage:
  install_hooks_into_repository.py [options] <path>

Options:
     --post-commit  Installs ``post-commit`` hook,
        that can be configuret to automatically update remote
        repository with some branch translation magic.
     --commit-msg  Installs ``commit-msg`` hook that will
        valdate commit message
     --update  Installs ``post-update`` and ``update`` hooks
        that will automatically merge branches pushed to this repository
     --pre-commit  Installs pre-commit hook that forbids commits
        to selected branches
     -c <file> --config-file=<file>  Installs config file
        specified by path. If unspecified will pass the default
        config file
"""
import logging

import os

from docopt import docopt, DocoptExit
import subprocess
import sys
import shutil

logging.basicConfig(level=logging.DEBUG)

OPTIONS = {
    '--commit-msg',
    '--post-commit',
    '--update',
    '--pre-commit'
}

HOOKS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'hooks'))


def get_git_dir(for_dir):
    """
    Tries to guess and returns working copy directory.
    """

    try:
        env = {k: v for (k, v) in os.environ.items() if 'GIT' not in k}
        git_dir = subprocess.check_output(
            "git rev-parse --git-dir".split(),
            cwd=for_dir, env=env)
        git_dir = git_dir.strip().decode('utf-8')
        if not os.path.isabs(git_dir.strip()):
            git_dir = os.path.join(for_dir, git_dir)
        return git_dir
    except subprocess.CalledProcessError:
        print("Directory is not inside git repository")
        sys.exit(1)


def update_link(from_file, to_file):
    if os.path.exists(to_file):
        print("EXISTS")
        subprocess.check_call(['rm', to_file])
    subprocess.check_call([
        'cp', from_file, to_file
    ])


def main():
    arguments = docopt(__doc__, version='Naval Fate 2.0', )
    print(arguments)

    config = os.path.join(HOOKS_DIR, '_hook_config_example.ini')

    if arguments['--config-file']:

        config = arguments['--config-file']

    if not os.path.exists(config):
        print("Config path {} does not exist".format(config))

    if not any([arguments[o] for o in OPTIONS]):
        print("Must pass at least one of {}".format(OPTIONS))
        raise DocoptExit()

    git_dir = get_git_dir(arguments['<path>'])
    print("Git dir is {}".format(git_dir))

    dest_dir = os.path.join(git_dir, 'hooks')

    if arguments['--commit-msg']:
        update_link(
            os.path.join(HOOKS_DIR, 'commit-msg.py'),
            os.path.join(dest_dir, 'commit-msg'))

    if arguments['--post-commit']:
        update_link(
            os.path.join(HOOKS_DIR, 'post-commit.py'),
            os.path.join(dest_dir, 'post-commit'))

    if arguments['--update']:
        update_link(
            os.path.join(HOOKS_DIR, 'update.py'),
            os.path.join(dest_dir, 'update'))
        update_link(
            os.path.join(HOOKS_DIR, 'update.py'),
            os.path.join(dest_dir, 'post-update'))

    if arguments['--pre-commit']:
        update_link(
            os.path.join(HOOKS_DIR, 'pre-commit.py'),
            os.path.join(dest_dir, 'pre-commit'))

    update_link(
        os.path.join(HOOKS_DIR, '_hook_config.py'),
        os.path.join(dest_dir, '_hook_config.py'))

    dest_config = os.path.join(dest_dir, "_hook_config.ini")

    if not os.path.exists(dest_config):
        shutil.copy(config, dest_config)
    else:
        logging.info("Config file exits will not override")

if __name__ == '__main__':
    main()