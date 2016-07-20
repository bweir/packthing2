from __future__ import print_function

import sys

def note(*objs):
    print(" NOTE:", *objs, file=sys.stderr)

def warn(*objs):
    print(" WARN:", *objs, file=sys.stderr)

def error(*objs):
    blocks = []
    for b in ' '.join(objs).split('\n'):
        if len(blocks) > 0:
            blocks.append("       "+b)
        else:
            blocks.append(b)

    print("ERROR:", "\n".join(blocks), file=sys.stderr)
    print()
    sys.exit(1)

