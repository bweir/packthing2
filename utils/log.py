from __future__ import print_function

import sys
import platform

_platform = platform.system().lower()

errors = []

_fail_on_error = False
_print_on_msg = False

def failOnError(enabled):
    global _fail_on_error
    _fail_on_error = enabled

def printOnError(enabled):
    global _print_on_error
    _print_on_error = enabled

def printErrors():
    global errors
    while errors:
        print(errors.pop(0), file=sys.stderr)

class Color:
    red     = '\033[0;31m'
    orange  = '\033[0;33m'
    yellow  = '\033[1;33m'
    green   = '\033[0;31m'
    white   = '\033[1;37m'
    off     = '\033[0m'

def render(*objs):
    blocks = []
    for b in ' '.join(objs).split('\n'):
        if len(blocks) > 0:
            blocks.append("       "+b)
        else:
            blocks.append(b)

    return "\n".join(blocks)

def msg(category, color, error, *objs):
    s = "[%-5s]: %s" % (category, render(*objs))
    if color and not _platform == "windows":
        s = color + s + Color.off

    if _print_on_msg:
        print(s, file=sys.stderr)
    else:
        errors.append(s)

    if error and _fail_on_error:
        sys.exit(1)

def note(*objs):
    msg("NOTE", Color.yellow, False, *objs)

def warn(*objs):
    msg("WARN", Color.orange, False, *objs)

def error(*objs):
    msg("ERROR", Color.red, True, *objs)
