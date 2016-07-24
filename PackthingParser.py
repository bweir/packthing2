from __future__ import print_function

import yaml
import keyengine as kk
import utils.log as log
import PackthingConfiguration as cfg
import PackthingImporter as importer

import platforms
import controllers
import builders
import packagers

kk.loadAll(platforms)
kk.loadAll(controllers)
kk.loadAll(builders)
kk.loadAll(packagers)

kk.dictionary("main")

kk.info("name",             "main",     kk.TEXT,        True)
kk.info("package",          "main",     kk.SLUG,        True)
kk.info("org",              "main",     kk.TEXT,        True)
kk.info("url",              "main",     kk.URL,         True)
kk.info("maintainer",       "main",     kk.TEXT,        True)
kk.info("email",            "main",     kk.EMAIL,       True)
kk.info("copyright",        "main",     kk.COPYRIGHT,   True)
kk.info("license",          "main",     kk.LICENSE,     True)
kk.info("tagline",          "main",     kk.TEXT,        True)
kk.info("description",      "main",     kk.TEXT,        True)
kk.info("master",           "main",     kk.SLUG,        False)

kk.dictionary("platform",   "main")
kk.dictionary("packager",   "main")
kk.dictionary("builder",    "main")

kk.collection("repo",       "main")

kk.info("url",              "repo",     kk.URL,         True)
kk.info("builder",          "repo",     kk.SLUG,        True)
kk.info("branch",           "repo",     kk.TEXT,        False)
kk.info("tag",              "repo",     kk.TEXT,        False)
kk.info("root",             "repo",     kk.PATH_REL,    False)

kk.collection("files",      "repo")

kk.info("name",             "files",    kk.TEXT,        True)
kk.info("icon",             "files",    kk.PATH_REL,    True)

kk.array("mimetype",        "main")

kk.info("type",             "mimetype", kk.TEXT,        True)
kk.info("extension",        "mimetype", kk.TEXT,        True)
kk.info("description",      "mimetype", kk.TEXT,        True)
kk.info("icon",             "mimetype", kk.TEXT,        True)
kk.info("files",            "mimetype", kk.TEXT,        True)



def getPackfile(d):
    log.failOnError(False)
    k = kk.dictionary("main")(d)
    log.printErrors()
#    k.visit()
#    log.abort()

def load(filename):
    try:
        return yaml.load(open(filename))
    except IOError:
        log.error("'"+self.repofile+"' not found; please specify a valid packthing file")

def parse(filename):

    d = load(filename)

    getPackfile(d)

#    print(kk.key_table)
