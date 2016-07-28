import PackthingParser as pp
import PackthingConfiguration as cfg

import PackthingImporter as importer
import keyengine as kk

import platforms
import packagers 

from utils import log

def add_config(names, group=None):
    for n in names:
        cfg.setting(n,  pp.find(n, group).value)


# collect main info

d = pp.load('packthing.yml')
pp.parse(d, "main")

add_config(["name",         "package",  "org",      "url",
            "maintainer",   "email",    "copyright","license",
            "tagline",      "description"], "main")

# collect platforms

platform = importer.module(cfg.value("platform"), platforms)

add_config(kk.keys(cfg.value("platform")), cfg.value("platform"))
platform.setup()
pp.parse(platform.tree(), "_platform_")

# collect controllers

def version():
    cfg.setting("version", "0.0.0")
    try:
        cfg.setting("version",  pp.find("version", "main").value)
    except AttributeError:
        pass
    cfg.override("version", "anothervalue")

version()

# collect builders

print(pp.findallvalues("builder", "repo"))

# collect packagers

def installer_name(package, version, arch, ext=None):
    s = package + "-" + version + "-" + arch
    if ext:
        s += "." + ext
    return s

packager = importer.module(cfg.value("packager"), packagers)
#packager.setup()

pp.parse(packager.tree(), "_packager_")
pp.parse(packager.tree(), "_packager_")

cfg.setting("installer", 
        installer_name(cfg.value("package"),
            cfg.value("version"),
            cfg.value("arch"),
            pp.find("ext", "_packager_").value))


cfg.printConfiguration()
