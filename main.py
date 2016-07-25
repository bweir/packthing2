import PackthingParser as pp
import PackthingConfiguration as cfg

import PackthingImporter as importer
import keyengine as kk

import platforms
import packagers 

from utils import log

d = pp.load('packthing.yml')
tree_main = pp.getTree(d, "main")

platform = importer.module(cfg.value("platform"), platforms)
platform.setup()

def version():
    cfg.setting("version", "0.0.0")
    try:
        cfg.setting("version",  kk.find(tree_main, "version", "main").value)
    except AttributeError:
        pass
    cfg.override("version", "anothervalue")

version()

cfg.setting("package",  kk.find(tree_main, "package", "main").value)

def installer_name(package, version, arch, ext=None):
    s = package + "-" + version + "-" + arch
    if ext:
        s += "." + ext
    return s

tree_platform = pp.getTree(platform.tree(), "_platform_")

packager = importer.module(cfg.value("packager"), packagers)
#packager.setup()

tree_packager = pp.getTree(packager.tree(), "_packager_")

cfg.setting("installer", 
        installer_name(cfg.value("package"),
            cfg.value("version"),
            cfg.value("arch"),
            kk.find(tree_packager, "ext", "_packager_").value))


cfg.printConfiguration()
