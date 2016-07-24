import PackthingParser as pp
import PackthingConfiguration as cfg

import PackthingImporter as importer

import platforms

#print("PLAT", importer.listPackages(platforms))
#print("BUILD", importer.listPackages(builders))
#print("CONT", importer.listPackages(controllers))
#print("PACK", importer.listPackages(packagers))
##print("MAA", importer.list_module_hierarchy(ckis))

pp.parse('packthing.yml')

#print cfg.allowed("platform")

platform = importer.module(cfg.value("platform"), platforms)
#print cfg.allowed("packager")
platform.setup()
#print cfg.allowed("packager")


cfg.printConfiguration()
