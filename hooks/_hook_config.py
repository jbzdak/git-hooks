
import os

import json

try:
    from ConfigParser import ConfigParser, NoSectionError, NoOptionError
except ImportError:
    from configparser import ConfigParser, NoSectionError, NoOptionError


DIRNAME = os.path.abspath(os.path.dirname(__file__))

cp = ConfigParser()
print(os.path.join(DIRNAME, "_hook_config.ini"))
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


def get_comma_separated_list(section, key, fallback):
    initial = get_fallback_cp(cp, section, key, fallback)
    splitted = initial.split(',')
    return [s for s in splitted if len(s.strip()) > 0]

POST_COMMIT_REMOTES_TO_UPDATE = get_comma_separated_list("update", 'remotes-to-update', 'origin,')

COMMIT_MSG_MIN_LENGTH = get_fallback_cp(cp, 'commit-msg', 'min-commit-length',
                                        fallback=15, method=ConfigParser.getint)

COMMIT_MSG_REQUIRED_REGEXPS = json.loads(get_fallback_cp(
    cp, 'commit-msg', 'required-regexps', fallback='[]'))

PRE_COMMMIT_FORBIDDEN_BRANCHES = get_comma_separated_list("pre-commit", 'forbid-commits-to', ',')

print(PRE_COMMMIT_FORBIDDEN_BRANCHES)