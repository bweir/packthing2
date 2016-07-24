import PackthingParser as pp
import PackthingConfiguration as cfg

import PackthingImporter as importer
import keyengine as kk

import platforms

pp.parse('packthing.yml')

platform = importer.module(cfg.value("platform"), platforms)
platform.setup()

pp.getPlatform(platform.project)

#cfg.printConfiguration()
