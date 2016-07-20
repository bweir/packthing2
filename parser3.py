from __future__ import print_function

import yaml
import util
import keyengine as kk
import importer

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


platforms = importer.module("platforms")
print(importer.listModules(platforms))

ckis = importer.listModules(platforms)

print("PACK", importer.listPackages(platforms))
print("MOD ", importer.listModules(platforms))
print("MAA", importer.list_module_hierarchy(ckis))

platforms = importer.module("chickn", platforms)
print (platforms)

#print( importer.get_modulelist(platform))
#print( get_module(parent, modulename) )
#print( list_module_hierarchy(module) )
#print( build_module_hierarchy(module) )


def getPlatform(config):
    import platforms.linux
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
        return kk.getKeyDict(config, "info")

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

