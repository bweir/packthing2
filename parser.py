from __future__ import print_function

import re
import yaml
import util
import pprint

RE_TEXT         = ".*"
RE_EMAIL        = "[^@]+@[^@]+\.[^@]+"
RE_URL          = "(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?"
RE_PATH_ABS     = "(/[^\\\]+)*"
RE_PATH_REL     = "[^\\\/]+"+RE_PATH_ABS
RE_SLUG         = "[a-z]*"
RE_CATEGORY     = "[a-z\-.]*"
RE_CATEGORIES   = "([a-zA-Z]+)(;[a-zA-Z]+)*"
RE_LICENSE      = "(MIT|GPLv3|BSD|Apache|GPLv2)"
RE_COPYRIGHT    = "[0-9]{4}(-[0-9]{4})?"

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

def getDeb(config):
    keylist = KeyList({
            "depends":      (optional,      str,    RE_TEXT,        "declare Debian package dependencies",              "libftdi1"),
            "categories":   (optional,      str,    RE_CATEGORIES,  "add your application to freedesktop categories",   "Development;IDE"),
            "section":      (optional,      str,    RE_TEXT,        "add application to debian menus",                  "Applications/Editors"),
            "help2man":     (getStringList, list,   RE_SLUG,        "generate man pages for binaris with help2man",     ""),
            })
    return getKeyList(config, keylist)

def getDmg(config):
    keylist = KeyList({
            "category":     (required,  str,    RE_CATEGORY,    "declare Mac app-category",                         "public.app-category.developer-tools"),
            "background":   (required,  str,    RE_PATH_REL,    "add a background image to the DMG installer",      "icons/mac-dmg.png"),
            "bundle":       (optional,  str,    RE_SLUG,        "specify which repo is the app bundle",             "Applications/Editors"),
            })
    return getKeyList(config, keylist)

def getInno(config):
    keylist = KeyList({
            "banner":       (required,  str,    RE_PATH_REL,    "add a banner image to the installer",              "icons/win-banner.bmp"),
            "run":          (optional,  str,    RE_TEXT,        "add option to run executable after installation",  "myexecutable"),
            })
    return getKeyList(config, keylist)

def getTarget(config):
    target = 'deb'

    keylist = KeyList({
            "deb":          (getDeb,    dict,   RE_SLUG,        "Debian package",           "awesome.deb"),
            "dmg":          (getDmg,    dict,   RE_SLUG,        "DMG volume",               "awesome.dmg"),
            "inno":         (getInno,   dict,   RE_SLUG,        "InnoSetup Installer",      ""),
            })

    if not target in keylist.keys():
        return {}

    return keylist.function(target)(config[target])

def getProject(config):
    keylist = KeyList({
            "name":         (required,  str,    RE_TEXT,        "pretty name of your project",              "Awesome Sauce"),
            "package":      (required,  str,    RE_SLUG,        "short package name of your project",       "awesomesauce"),
            "org":          (required,  str,    RE_TEXT,        "organization",                             "Acme Inc."),
            "url":          (required,  str,    RE_URL,         "project website URL",                      "http://www.example.com"),
            "maintainer":   (required,  str,    RE_TEXT,        "name of the project maintainer",           "Sam Smith"),
            "email":        (required,  str,    RE_EMAIL,       "email address of the project maintainer",  "samsmith@smithysmith.com"),
            "copyright":    (required,  str,    RE_COPYRIGHT,   "copyright year of application",            "2014-2015"),
            "license":      (required,  str,    RE_LICENSE,     "release license of the software",          "GPLv3, MIT, ..."),
            "tagline":      (required,  str,    RE_TEXT,        "short one-line description of project",    "the most awesome thing ever"),
            "description":  (required,  str,    RE_TEXT,        "longer description of project",            "Awesome Sauce is a unified integrator of fazzbizz componenents"),
            "master":       (optional,  str,    RE_SLUG,        "master project in repository list",        "awesomesauce"),
            "target":       (getTarget, dict,   "",             "",                                         ""),
            "repos":        (getRepos,  dict,   "",             "",                                         ""),
            })
    return getKeyList(config, keylist)


def load(filename):
    try:
        return yaml.load(open(filename))
    except IOError:
        util.error("'"+self.repofile+"' not found; please specify a valid packthing file")

def parse(filename):

    config = load(filename)
    config = getProject(config)

    #pprint.pprint(config)
    print(yaml.safe_dump(config))

parse('packthing.yml')
