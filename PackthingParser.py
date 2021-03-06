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

def loadall(package):
    for m in importer.listModules(package):
        importer.module(m, package)

loadall(platforms)
loadall(controllers)
loadall(builders)
loadall(packagers)

# main packfile support

kk.dictionary("main")

kk.info("name",             "main",         kk.TEXT,        True)
kk.info("package",          "main",         kk.SLUG,        True)
kk.info("org",              "main",         kk.TEXT,        True)
kk.info("url",              "main",         kk.URL,         True)
kk.info("maintainer",       "main",         kk.TEXT,        True)
kk.info("email",            "main",         kk.EMAIL,       True)
kk.info("copyright",        "main",         kk.COPYRIGHT,   True)
kk.info("license",          "main",         kk.LICENSE,     True)
kk.info("tagline",          "main",         kk.TEXT,        True)
kk.info("description",      "main",         kk.TEXT,        True)
kk.info("master",           "main",         kk.SLUG,        False)
kk.info("version",          "main",         kk.TEXT,        False)

# platform support

kk.dictionary("platform",   "main")

# internal platform support

kk.dictionary("_platform_")

kk.dictionary("ext",        "_platform_")

kk.info("bin",              "ext",          kk.NSLUG,       True)
kk.info("lib",              "ext",          kk.NSLUG,       True)

kk.dictionary("prefix",     "_platform_")

kk.info("lib",              "prefix",       kk.NSLUG,       True)

kk.dictionary("path",       "_platform_")

kk.info("bin",              "path",         kk.PATH_REL,    True)
kk.info("lib",              "path",         kk.PATH_REL,    True)
kk.info("share",            "path",         kk.PATH_REL,    True)

# packager support

kk.dictionary("packager",   "main")

# internal packager support

kk.dictionary("_packager_")

kk.info("ext",              "_packager_",   kk.SLUG,    True)

# builder support

kk.dictionary("builder",    "main")

# controller support

kk.collection("repo",       "main")

kk.info("url",              "repo",         kk.URL,         True)
kk.info("builder",          "repo",         kk.SLUG,        True)
kk.info("branch",           "repo",         kk.TEXT,        False)
kk.info("tag",              "repo",         kk.TEXT,        False)
kk.info("root",             "repo",         kk.PATH_REL,    False)

kk.collection("files",      "repo")

kk.info("name",             "files",        kk.TEXT,        True)
kk.info("icon",             "files",        kk.PATH_REL,    True)

# mimetype support

kk.array("mimetype",        "main")

kk.info("type",             "mimetype",     kk.TEXT,        True)
kk.info("extension",        "mimetype",     kk.TEXT,        True)
kk.info("description",      "mimetype",     kk.TEXT,        True)
kk.info("icon",             "mimetype",     kk.TEXT,        True)
kk.info("files",            "mimetype",     kk.TEXT,        True)

tree_table = []

def parse(d, root=None):
    log.failOnError(False)
    log.printOnError(False)
    tree = kk.dictionary(root)(d)
    log.printErrors()
    log.failOnError(True)
    log.printOnError(True)
    add_root(tree)
#    print(k.collect(kk.key("files", "mimetype")))
#
#    print(k.collect(kk.key("help2man", "linux")))
#
#    for v in k.collect(kk.key("mimetype", "mimetype")):
#        print(v.value["files"])
#
#    for v in k.collect(kk.key("repo", "main")):
#        for n in v.value:
#            print (v.value[n]["url"].value)

#    print(k, k.collect)
#    log.abort()

    return tree

def load(filename):
    try:
        return yaml.load(open(filename))
    except IOError:
        log.error("'"+self.repofile+"' not found; please specify a valid packthing file")

def add_root(tree):
    if not tree.group == None:
        log.error("Not root tree:", tree.name)

    for t in tree_table:
        if t.name == tree.name:
            log.note("Root tree is defined twice:", tree.name)

    tree_table.append(tree)

def findall(name, group=None):
    items = []
    for t in tree_table:
        try:
            items.extend(t.collect(kk.key(name, group)))
        except IndexError:
            pass
    return items

def find(name, group=None):
    try:
        return findall(name, group)[0]
    except IndexError:
        return None

def findallvalues(name, group=None):
    items = findall(name, group)
    newitems = []
    for i in items:
        if i.value not in newitems:
            newitems.append(i.value)
    return newitems

