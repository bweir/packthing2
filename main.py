import PackthingParser as pp
import PackthingConfiguration as cfg

import PackthingImporter as importer
import keyengine as kk

import platforms

d = pp.load('packthing.yml')
pp.getPackfile(d)

platform = importer.module(cfg.value("platform"), platforms)
platform.setup()

pp.getPlatform(platform.platform())

#cfg.printConfiguration()
