from __future__ import print_function
import sys
import util
import pkgutil, importlib
import inspect

from types import ModuleType

_platform = util.get_platform()

def module(name, parent=None):
    if parent == None:
        try:
            return importlib.import_module(name)
        except ImportError:
            util.error("No module named '"+name+"'")
    else:
        if not type(parent) == ModuleType:
            util.error("Module '"+str(parent)+"' is not a module!")

        try:
            return importlib.import_module(parent.__name__+'.'+name)
        except ImportError:
            util.error("No module named '"+name+"' in '"+parent.__name__+"'")


def listPackages(package):
    return listModules(package, True)

def listModules(package, ispkg=False):
    modules = []
    for p in pkgutil.iter_modules(package.__path__, package.__name__+'.'):
        if p[2] == ispkg:
            modules.append(p[1])

    for i in range(len(modules)):
        modules[i] = modules[i].split('.')[-1]

    return modules

def list_module_hierarchy(module):
    clsmembers = inspect.getmembers(module, inspect.isclass)
    return inspect.getmro(clsmembers[0][1])

def build_module_hierarchy(module):
    clsmembers = inspect.getmembers(module, inspect.isclass)
    parenttree = inspect.getmro(clsmembers[0][1])

    modulelist = []
    for p in parenttree:
        modulelist.append(importlib.import_module(p.__module__))
    modulelist.append(module)

    return modulelist


def require(module):
    if _platform['system'] == 'windows': # REQUIRE DOESN'T WORK ON WINDOWS
        return

    for m in build_module_hierarchy(module):
        try:
            m.REQUIRE
        except AttributeError as e:
            continue

        for r in m.REQUIRE:
            found = util.which(r)
            if not found:
                util.error("Required program '"+r+"' not available")

def required_keys(module):
    keylist = []
    for m in build_module_hierarchy(module):
        try:
            keylist.extend(m.KEYS)
        except AttributeError as e:
            continue
    return list(set(keylist))
