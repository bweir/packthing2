from __future__ import print_function

import platform

import platforms
import packagers
import builders
import controllers

import utils.log as log

import PackthingImporter as importer

config_table = {}
override_table = {}
allowed_table = {}

class ConfigBase(object):
    name = None

    def __repr__(self):
        return "((%s) %s: %s)" % (self.group, self.name, self.value())

    def value(self):
        try:
            return override_table[self.name]
        except KeyError:
            return self.default()

    def allow(self, value):
        assert isinstance(value, list)
        for v in value:
            newv = []
            if v in self.supported():
                newv.append(v)
            else:
                log.warn("Excluding unsupported "+self.name+" value '"+v+"'")
        allowed_table[self.name] = newv

    def allowed(self):
        try:
            return allowed_table[self.name]
        except KeyError:
            return self.supported()

    def supported(self):
        log.warn("No supported values for config item '"+self.name+"'")
        return []

    def default(self):
        if len(self.allowed()) == 1:
            return self.allowed()[0]
        else:
            return ""

def config(name):
    try:
        k = config_table[name]
    except KeyError:
        class k(ConfigBase):
            pass
        k.__name__ = name
        k.name = name 
        config_table[name] = k
    return k

def setting(name, value):
    def default(self):
        return self._value

    def supported(self):
        return [self._value]

    k = config(name)
    k._value = value
    k.default = default
    k.supported = supported
    config_table[name] = k

def method(k):
    assert issubclass(k, ConfigBase)
    def bind(fn):
        setattr(k, fn.__name__, fn)
    return bind

config("arch")
config("platform")
config("packager")

@method(config("arch"))
def supported(self):    return ["i686", "amd64", "armhf", "armel"]

@method(config("arch"))
def default(self):      return platform.processor().replace("x86_64", "amd64")



@method(config("packager"))
def supported(self):    return importer.listModules(packagers)

@method(config("builder"))
def supported(self):    return importer.listModules(builders)

@method(config("controller"))
def supported(self):    return importer.listModules(controllers)


@method(config("platform"))
def supported(self):    return importer.listModules(platforms)

@method(config("platform"))
def default(self):
    v = platform.system().lower().replace("darwin", "mac")
    if not v in config("platform")().allowed():
        log.error("No platform '"+v+"' in platforms")
    return v



def keys():
    return config_table.keys()

def value(configname):
    return config(configname)().value()

def allowed(configname):
    return config(configname)().allowed()

def allow(name, value):
    return config(name)().allow(value)

def override(configname, value):
    if not configname in config_table:
        log.error("Attempting to override undefined value:",configname)

    override_table[configname] = value

def printConfiguration():
    ks = keys()
    ks.sort()
    for k in ks:
        v = value(k)
#        if not v:
#            v = "No "+k+" selected"
        try:
            print ("  %-20s: %-40s [%s]" % (k, v, ', '.join(allowed(k))))
        except TypeError:
            print ("  %-20s: %-40s [%s]" % (k, v, allowed(k)))

    log.printErrors()


