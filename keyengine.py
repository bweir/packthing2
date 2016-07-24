from __future__ import print_function

import PackthingImporter as importer
import PackthingCoreObject as core

import utils.log as log
import utils.test as tf

TEXT        = ".*"
EMAIL       = "[^@]+@[^@]+\.[^@]+"
SLUG        = "[a-z]+"
NSLUG       = "[a-z]*"
PATH_ABS    = "(/[^\\\]+)*"
PATH_REL    = "[^\\\/]+"+PATH_ABS
CATEGORY    = "[a-z\-.]*"
CATEGORIES  = "([a-zA-Z]+)(;[a-zA-Z]+)*"
LICENSE     = "(MIT|GPLv3|BSD|Apache|GPLv2)"
COPYRIGHT   = "[0-9]{4}(-[0-9]{4})?"
URL         = "(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?"

key_table = {}
push_stack = 0


class KeyBase(object):
    name = None
    group = None
    value = None
    required = None

    def __repr__(self):
        return "(%s (%s): %s)" % (self.name, self.group, self.value)

    def __init__(self, value):
        self.value = value

    def visit(self):
        print (self)

    def collect(self, classtype):
        if isinstance(self, classtype):
            return [self]
        else:
            return []

def key(name, group=None):
    keys(group)

    try:
        k = key_table[group][name]
    except KeyError:
        class k(KeyBase):
            pass
        k.__name__ = name
        k.name = name 
        k.group = group
#        k.value = None
        key_table[group][name] = k

    return k

def method(k):
    assert issubclass(k, KeyBase)
    def bind(fn):
        setattr(k, fn.__name__, fn)
    return bind

def groups():
    return key_table.keys()

def keys(group=None):
    try:
        key_table[group]
    except KeyError:
        key_table[group] = {}
    return key_table[group].keys()

def required(a, group=None, name=None):
    k = key(a, group)
    if k.required == True:
        if name:
            log.error("Missing '"+a+"' key in "+group+" '"+name+"'")
        else:
            log.error("Missing key '"+a+"' in group '"+group+"'")

def newDict(value, group=None, name=None):
    available = keys(group)

    d = {}
    for k, v in value.items():
        try:
            available.remove(k)
        except ValueError:
            log.error("Key '"+k+"' not valid in '"+group+"' group")

        if isinstance(v, dict):
            d[k] = dictionary(k, group)(v)
        elif isinstance(v, list):
            d[k] = array(k, group)(v)
        elif isinstance(v, str):
            d[k] = key(k, group)(v)
        else:
            log.warn("Group '"+k+"' has no keys")

    for a in available:
        required(a, group, name)

    return d


def newkey(fn):
    def bind(name, group=None, *args): 
        try:
            return key_table[group][name]
        except KeyError:
            k = fn(name, group, *args)
            key_table[group][name] = k
            return k
    return bind


@newkey
def info(name, group=None, pattern=TEXT, required=False):
    def __init__(self, value):
        tf.isType(self.name, value, str)
        tf.isEmpty(self.name, value)
        tf.isMatch(self.name, value, pattern)
        self.value = value

    def visit(self):
        print(push_stack, "  "*push_stack, self)

    k = key(name, group)
    k.__init__ = __init__
    k.visit = visit
    k.pattern = pattern
    k.required = required
    return k


@newkey
def infoList(name, group=None, pattern=TEXT):
    def __init__(self, value):
        if isinstance(value, str):
            tf.isType(self.name, value, str)
            tf.isEmpty(self.name, value)
            tf.isMatch(self.name, value, pattern)
            self.value = [value]
        elif isinstance(value, list):
            self.value = []
            for v in value:
                tf.isType(self.name, value, str)
                tf.isEmpty(self.name, value)
                tf.isMatch(self.name, value, pattern)
                self.value.append(v)

    def visit(self):
        print(push_stack, "  "*push_stack, self.name+": ["+', '.join(self.value)+"]")

    k = key(name, group)
    k.__init__ = __init__
    k.visit = visit
    k.pattern = pattern
    return k


@newkey
def dictionary(name, group=None):
    def __init__(self, value):
        tf.isType(self.name, value, dict)
        self.value = newDict(value, name)

    def visit(self):
        global push_stack
        print(push_stack, "  "*push_stack, self.name)

        push_stack += 1

        for k, v in self.value.items():
            v.visit()

        push_stack -= 1

    def collect(self, classtype):
        l = []

        if isinstance(self, classtype):
            l.append(self)

        for k, v in self.value.items():
            l.extend(v.collect(classtype))

        return l

    k = key(name, group)
    k.visit = visit
    k.collect = collect
    k.__init__ = __init__
    return k

@newkey
def array(name, group=None):
    def __init__(self, value):
        tf.isType(self.name, value, list)

        self.value = []
        for v in value:
            self.value.append(dictionary(name, name)(v))

    def visit(self):
        global push_stack
        print(push_stack, "  "*push_stack, self.name)

        push_stack += 1

        for v in self.value:
            v.visit()

        push_stack -= 1

    def collect(self, classtype):
        l = []

        if isinstance(self, classtype):
            l.append(self)

        for v in self.value:
            l.extend(v.collect(classtype))

        return l

    k = key(name, group)
    k.visit = visit
    k.collect = collect
    k.__init__ = __init__
    return k

@newkey
def collection(name, group=None):
    def __init__(self, value):
        tf.isType(self.name, value, dict)
        
        self.value = {}
        for k, v in value.items():
            self.value[k] = newDict(v, name, k)

    def visit(self):
        global push_stack
        print(push_stack, "  "*push_stack, self.name)

        push_stack += 1
        for k, v in self.value.items():
            print(push_stack, "  "*push_stack, k)

            push_stack += 1
            for subk, subv in v.items():
                subv.visit()

            push_stack += -1
        push_stack += -1

    def collect(self, classtype):
        l = []

        if isinstance(self, classtype):
            l.append(self)

        for k, v in self.value.items():
            for subk, subv in v.items():
                l.extend(subv.collect(classtype))

        return l

    k = dictionary(name, group)
    k.visit = visit
    k.collect = collect
    k.__init__ = __init__
    return k


def loadAll(package):
    for m in importer.listModules(package):
        importer.module(m, package)

