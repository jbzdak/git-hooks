#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage:
    install_hooks_into_repository.py [options] TARGET_DIR

Options:
   --install-post-commit  Installs post commit hook, that can be configuret to automatically update remote repository with some branch translation magic.
   --install-message  Installs ``commit-msg`` hook that will
    valdate commit message
   --install-update  Installs ``post-update`` and ``update`` hooks
    that will automatically merge branches pushed to this repository.
"""

import docopt

from docopt import docopt

def main():
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)

if __name__ == '__main__':
    main()