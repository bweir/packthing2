import yaml
import pprint
import util
import parsercore as core
import constants as cc

from packagers import deb

def getDmg(config):
    keylist = core.KeyList({
            "category":     (core.required,  str,    cc.RE_CATEGORY,    "declare Mac app-category",                         "public.app-category.developer-tools"),
            "background":   (core.required,  str,    cc.RE_PATH_REL,    "add a background image to the DMG installer",      "icons/mac-dmg.png"),
            "bundle":       (core.optional,  str,    cc.RE_SLUG,        "specify which repo is the app bundle",             "Applications/Editors"),
            })
    return core.getKeyList(config, keylist)

def getInno(config):
    keylist = core.KeyList({
            "banner":       (core.required,  str,    cc.RE_PATH_REL,    "add a banner image to the installer",              "icons/win-banner.bmp"),
            "run":          (core.optional,  str,    cc.RE_TEXT,        "add option to run executable after installation",  "myexecutable"),
            })
    return core.getKeyList(config, keylist)


def getTarget(config):
    target = 'deb'

    if not target in config:
        return {}

    try:
        return deb.parse(config[target])
    except AttributeError:
        util.error("Target '"+target+"' does not support platform-specific keys.")


def getProject(config):
    keylist = core.KeyList({
            "name":         (core.required,  str,    cc.RE_TEXT,     "pretty name of your project",              "Awesome Sauce"),
            "package":      (core.required,  str,    cc.RE_SLUG,     "short package name of your project",       "awesomesauce"),
            "org":          (core.required,  str,    cc.RE_TEXT,     "organization",                             "Acme Inc."),
            "url":          (core.required,  str,    cc.RE_URL,      "project website URL",                      "http://www.example.com"),
            "maintainer":   (core.required,  str,    cc.RE_TEXT,     "name of the project maintainer",           "Sam Smith"),
            "email":        (core.required,  str,    cc.RE_EMAIL,    "email address of the project maintainer",  "samsmith@smithysmith.com"),
            "copyright":    (core.required,  str,    cc.RE_COPYRIGHT,"copyright year of application",            "2014-2015"),
            "license":      (core.required,  str,    cc.RE_LICENSE,  "release license of the software",          "GPLv3, MIT, ..."),
            "tagline":      (core.required,  str,    cc.RE_TEXT,     "short one-line description of project",    "the most awesome thing ever"),
            "description":  (core.required,  str,    cc.RE_TEXT,     "longer description of project",            "Awesome Sauce is a unified integrator of fazzbizz componenents"),
            "master":       (core.optional,  str,    cc.RE_SLUG,     "master project in repository list",        "awesomesauce"),
            "target":       (getTarget,     dict,   "",             "",                                         ""),
            "repos":        (core.getRepos, dict,   "",             "",                                         ""),
            })
    return core.getKeyList(config, keylist)


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

