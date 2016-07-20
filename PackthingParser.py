from __future__ import print_function

import yaml
import keyengine as kk
import utils.log as log
from PackthingConfiguration import Configuration as cfg
import importer

import platforms
import packagers
import builders
import controllers

kk.key("info", "name",             True,   str, kk.TEXT)
kk.key("info", "package",          True,   str, kk.SLUG)
kk.key("info", "org",              True,   str, kk.TEXT)
kk.key("info", "url",              True,   str, kk.URL)
kk.key("info", "maintainer",       True,   str, kk.TEXT)
kk.key("info", "email",            True,   str, kk.EMAIL)
kk.key("info", "copyright",        True,   str, kk.COPYRIGHT)
kk.key("info", "license",          True,   str, kk.LICENSE)
kk.key("info", "tagline",          True,   str, kk.TEXT)
kk.key("info", "description",      True,   str, kk.TEXT)
kk.key("info", "master",           False,  str, kk.SLUG)
kk.key("info", "repos",            False,  dict, kk.SLUG)

#print(importer.listModules(platforms))
#
#ckis = importer.listModules(platforms)
#
print("PLAT", importer.listPackages(platforms))
print("BUILD", importer.listPackages(builders))
print("CONT", importer.listPackages(controllers))
print("PACK", importer.listPackages(packagers))
#print("MAA", importer.list_module_hierarchy(ckis))

def getScope(config, key, package):
    scope = cfg.value(key)
    config = kk.loadModule(config, key, scope, package)
    config = kk.mergeKeys(config, key, scope)
    return config

def getPlatform(config):
    config = getScope(config, "platform", platforms)
    config = getInfo(config)
    return config

def getPackager(config):
    config = getScope(config, "packager", packagers)
    config = getInfo(config)
    return config

def getInfo(config):
    if "platform" in config:
        return getPlatform(config)
    elif "packager" in config:
        return getPackager(config)
    else:
        return kk.getKeyDict(config, "info")

def load(filename):
    try:
        return yaml.load(open(filename))
    except IOError:
        log.error("'"+self.repofile+"' not found; please specify a valid packthing file")

def parse(filename):

    config = load(filename)
    config = getInfo(config)

    print(kk.key_table)

    for c in config:
        print(config[c])
