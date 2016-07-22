import platform

import platforms
import packagers
import builders
import controllers

import utils.log as log

import PackthingImporter as importer

key_table = {}
override_table = {}

class ConfigBase(object):
    name = None

    def __repr__(self):
        return "((%s) %s: %s)" % (self.group, self.name, self.value())

    def value(self):
        try:
            return override_table[self.name]
        except KeyError:
            return self.default()

    def default(self):
        return ""

def key(name):
    try:
        k = key_table[name]
    except KeyError:
        class k(ConfigBase):
            pass
        k.__name__ = name
        k.name = name 
        key_table[name] = k
    return k

def method(k):
    assert issubclass(k, ConfigBase)
    def bind(fn):
        setattr(k, fn.__name__, fn)
    return bind

key("arch")
key("platform")
key("packager")

@method(key("platform"))
def default(self):
    v = platform.system().lower().replace("darwin", "mac")
    systems = importer.listModules(platforms)
    if not v in systems:
        log.error("No platform '"+v+"' in platforms")
    return v

@method(key("arch"))
def default(self):
    return platform.processor().replace("x86_64", "amd64")



def keys():
    return key_table.keys()

def value(keyname):
    return key(keyname)().value()

def override(keyname, value):
    if not keyname in key_table:
        log.error("Attempting to override undefined value:",keyname)

    override_table[keyname] = value
