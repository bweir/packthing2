from utils import log

import re

def isMissingKeys(keylist):
    if len(_missingkeys):
        msg = "The following keys are missing from the packfile!\n"
        for k in _missingkeys:
            msg += "\n- %-16s %-50s (e.g. %s)" % (k,
                    keylist.description(k),
                    keylist.example(k))
        log.error(msg)

def isType(key, value, expected):
    try:
        assert isinstance(value, expected)
    except AssertionError:
        log.error("Key '"+key+"' is of type '"+type(value).__name__+"';",
                   "expected '"+expected.__name__+"'.",
                   "(value: "+str(value)+")")

def isEmpty(key, value):
    if value == None:
        log.warn("'"+key+"' is defined but empty") 

def isMatch(key, value, pattern):
    try:
        if not re.compile("^"+pattern+"$").match(value):
            log.error(key+"' value '"+value+"' does not match pattern '"+pattern+"'")
    except TypeError:
        log.error("Invalid type for '"+key+"' value: "+str(value))

