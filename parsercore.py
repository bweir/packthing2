from __future__ import print_function

import re
import util
import constants as cc

class KeyList:
    def __init__(self, keylist):
        self.keylist = keylist 

    def entry(self, key):
        entry = self.keylist.get(key, None)

        if entry == None:
            util.error("Invalid key '"+key+"' found in packfile") 
        
        return entry

    def keys(self):
        return self.keylist.keys()

    def value(self, key, num):
        return self.entry(key)[num]

    def function(self, key):
        return self.value(key, 0)

    def valuetype(self, key):
        return self.value(key, 1)

    def pattern(self, key):
        return self.value(key, 2)

    def description(self, key):
        return self.value(key, 3)

    def example(self, key):
        return self.value(key, 4)

_missingkeys = []

def testMissingKeys(keylist):
    if len(_missingkeys):
        msg = "The following keys are missing from the packfile!\n"
        for k in _missingkeys:
            msg += "\n- %-16s %-50s (e.g. %s)" % (k,
                    keylist.description(k),
                    keylist.example(k))
        util.error(msg)

def testType(key, value, expected):
    if not type(value) is expected:
        util.error("Key '"+key+"' is of type '"+type(value).__name__+"';",
                   "expected '"+expected.__name__+"'.",
                   "(value: "+str(value)+")")

def testEmpty(key, value):
    if value == "" or value == None:
        util.error("'"+key+"' is defined but empty") 

def testMatch(key, value, pattern):
    regex = re.compile("^"+pattern+"$")
    try:
        if not regex.match(value):
            util.error(key+"' value '"+value+"' does not match pattern '"+pattern+"'")
    except TypeError:
        util.error("Invalid type for '"+key+"' value: "+str(value))

def getKey(config, keylist, key):
    keylist.entry(key)
    testEmpty(key, config[key])
    testType(key, config[key], keylist.valuetype(key))
    testMatch(key, config[key], keylist.pattern(key))

    return config[key]


def required(config, keylist, key):

    if not key in config:
        global _missingkeys
        _missingkeys.append(key)
        return ""

    return getKey(config, keylist, key)

def optional(config, keylist, key):

    if not key in config:
        return ""

    return getKey(config, keylist, key)


def getKeyList(config, keylist):
    if config == None:
        return {}

    newconfig = {}

    for k in config.keys():

        valtype = keylist.valuetype(k)
        
        if valtype is dict:
            newconfig.update(keylist.function(k)(config[k]))
        elif valtype is list:
            newconfig[k] = keylist.function(k)(config[k], k, keylist.pattern(k))
        elif valtype is None:
            pass
        else:
            newconfig[k] = keylist.function(k)(config, keylist, k)

    testMissingKeys(keylist)

    return newconfig

def getStringList(config, key, pattern):
    if config == None:
        return []

    if type(config) is str:
        testMatch(key, config, pattern)
        return [config]

    newconfig = []

    for value in config:
        testEmpty(key, value)
        testType(key, value, str)
        testMatch(key, value, pattern)
        newconfig.append(value)

    return newconfig

def getRepos(config):
    return {"repos": config}

