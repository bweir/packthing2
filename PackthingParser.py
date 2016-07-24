from __future__ import print_function

import yaml
import keyengine as kk
import utils.log as log
import PackthingConfiguration as cfg
import PackthingImporter as importer

import platforms
import packagers
import builders
import controllers

kk.dictionary("main")

kk.info("name",             "main",     kk.TEXT)
kk.info("package",          "main",     kk.SLUG)
kk.info("org",              "main",     kk.TEXT)
kk.info("url",              "main",     kk.URL)
kk.info("maintainer",       "main",     kk.TEXT)
kk.info("email",            "main",     kk.EMAIL)
kk.info("copyright",        "main",     kk.COPYRIGHT)
kk.info("license",          "main",     kk.LICENSE)
kk.info("tagline",          "main",     kk.TEXT)
kk.info("description",      "main",     kk.TEXT)
kk.info("master",           "main",     kk.SLUG)

kk.collection("platform",   "main")
kk.collection("packager",   "main")
kk.collection("builder",    "main")

kk.collection("repo",       "main")

kk.info("url",              "repo",     kk.URL)
kk.info("builder",          "repo",     kk.SLUG)
kk.info("branch",           "repo",     kk.TEXT)
kk.info("tag",              "repo",     kk.TEXT)
kk.info("root",             "repo",     kk.PATH_REL)

kk.collection("files",      "repo")

kk.info("name",             "files",    kk.TEXT)
kk.info("icon",             "files",    kk.PATH_REL)

kk.array("mimetype",        "main")

kk.info("type",             "mimetype")
kk.info("extension",        "mimetype")
kk.info("description",      "mimetype")
kk.info("icon",             "mimetype")
kk.info("files",            "mimetype")

def getScope(config, key, package):
    scope = cfg.value(key)
    config = kk.loadModule(config, key, scope, package)
    config = kk.mergeKeys(config, key, scope)
    return config

def getPlatform(config, group):
    config = getScope(config, "platform", platforms)
    config = getGroup(config, group)
    return config

def getPackager(config, group):
    config = getScope(config, "packager", packagers)
    config = getGroup(config, group)
    return config

def getGroup(config, group):
    for k in kk.keys(group):
        if k == "platform":
            config = getPlatform(config, group)
        elif k == "packager":
            config = getPackager(config, group)
        elif k == "repos":
            config = getRepos(config, group)
        else:
            return kk.getKeyDict(config, group)

def getRepos(config):
    repos = {}

#    for c in config.keys():
#        print (c, config[c])

    return repos

#def getDict(d, group=None):
#    for k, v in d.items():
#        if k in kk.keys(group):
#            kk.key(k)(v).visit()
##        else:
##            log.error("OIDFJID", k, v)

def getPackfile(d):
    k = kk.dictionary("main")(d)
    k.visit()

def load(filename):
    try:
        return yaml.load(open(filename))
    except IOError:
        log.error("'"+self.repofile+"' not found; please specify a valid packthing file")

def parse(filename):

    d = load(filename)
    #config = getGroup(config, "info")
#    config = getGroup(config, "info")

    getPackfile(d)

#    print(kk.key_table)
#
#    for c in config:
#        print(config[c])
