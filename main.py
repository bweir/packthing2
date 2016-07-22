import PackthingParser as pp
import PackthingConfiguration as cfg

#print(importer.listModules(platforms))
#ckis = importer.listModules(platforms)

#print("PLAT", importer.listPackages(platforms))
#print("BUILD", importer.listPackages(builders))
#print("CONT", importer.listPackages(controllers))
#print("PACK", importer.listPackages(packagers))
##print("MAA", importer.list_module_hierarchy(ckis))

for k in cfg.keys():
    print "%10s: %s" % (k, cfg.value(k))

pp.parse('packthing.yml')

