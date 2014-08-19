
import os

import json

try:
    from ConfigParser import ConfigParser, NoSectionError, NoOptionError
except ImportError:
    from configparser import ConfigParser, NoSectionError, NoOptionError


DIRNAME = os.path.dirname(__name__)

cp = ConfigParser()
cp.read(os.path.join(DIRNAME, "_hook_config.ini"))

_NO_FALLBACK = object()


def get_fallback_cp(cp, section, name, fallback=_NO_FALLBACK, method=ConfigParser.get):

    try:
        return method(cp, section, name)
    except (NoOptionError, NoSectionError):
        if fallback != _NO_FALLBACK:
            return fallback
        raise

SHARED_AUTOMERGE_SUFFIX = get_fallback_cp(cp, "shared", 'automerge-suffix', '-automerge')


def _get_force_working_dir():

    initial = get_fallback_cp(cp, "update", 'force-working-dir', 'none')
    if initial.lower() == 'none':
        return None
    return initial

UPDATE_FORCE_WORKING_DIR = _get_force_working_dir()

UPDATE_CAN_GUESS_GIT_WORK_TREE = get_fallback_cp(
    cp, "update", 'can-guess-git-work-tree', False,
    method=ConfigParser.getboolean)


def _get_remotes_to_update():
    initial = get_fallback_cp(cp, "update", 'remotes-to-update', 'origin,')
    splitted = initial.split(',')
    return [s for s in splitted if len(s.strip()) > 0]

POST_COMMIT_REMOTES_TO_UPDATE = _get_remotes_to_update()

COMMIT_MSG_MIN_LENGTH = get_fallback_cp(cp, 'commit-msg', 'min-commit-length',
                                        fallback=15, method=ConfigParser.getint)

COMMIT_MSG_REQUIRED_REGEXPS = json.loads(get_fallback_cp(
    cp, 'commit-msg', 'required-regexps', fallback='[]'))
