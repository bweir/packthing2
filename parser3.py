from __future__ import print_function

import yaml
import util
import re
import keyengine as kk


kk.key("name",             True,   str, kk.TEXT)
kk.key("package",          True,   str, kk.SLUG)
kk.key("org",              True,   str, kk.TEXT)
kk.key("url",              True,   str, kk.URL)
kk.key("maintainer",       True,   str, kk.TEXT)
kk.key("email",            True,   str, kk.EMAIL)
kk.key("copyright",        True,   str, kk.COPYRIGHT)
kk.key("license",          True,   str, kk.LICENSE)
kk.key("tagline",          True,   str, kk.TEXT)
kk.key("description",      True,   str, kk.TEXT)
kk.key("master",           False,  str, kk.SLUG)

def getPlatform(config):
    import ptplatform.linux
    config = kk.mergeKeys(config, "platform", "linux")
    config = getInfo(config)
    return config

def getPackager(config):
    config = kk.mergeKeys(config, "packager", "deb")
    config = getInfo(config)
    return config

def getInfo(config):
    if "platform" in config:
        return getPlatform(config)
    elif "packager" in config:
        return getPackager(config)
    else:
        return kk.getKeyDict(config)

def load(filename):
    try:
        return yaml.load(open(filename))
    except IOError:
        util.error("'"+self.repofile+"' not found; please specify a valid packthing file")

def parse(filename):

    config = load(filename)
    config = getInfo(config)

    print(kk.key_table)

    for c in config:
        print(config[c])

parse('packthing.yml')

