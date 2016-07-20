import PackthingParser as pp
from PackthingConfiguration import Configuration as cfg

cfg.packager = "deb"
cfg.arch = "windows"
pp.parse('packthing.yml')

