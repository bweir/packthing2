from __future__ import print_function

import utils.log as log
import utils.test as tf

TEXT        = ".*"
EMAIL       = "[^@]+@[^@]+\.[^@]+"
SLUG        = "[a-z]+"
PATH_ABS    = "(/[^\\\]+)*"
PATH_REL    = "[^\\\/]+"+PATH_ABS
CATEGORY    = "[a-z\-.]*"
CATEGORIES  = "([a-zA-Z]+)(;[a-zA-Z]+)*"
LICENSE     = "(MIT|GPLv3|BSD|Apache|GPLv2)"
COPYRIGHT   = "[0-9]{4}(-[0-9]{4})?"
URL         = "(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?"

key_table = {}

class KeyBase(object):
    name = None
    group = None
    value = None

    def visit(self):
#        print (k, v)
        print (self)

    def __repr__(self):
        return "(%s (%s): %s)" % (self.name, self.group, self.value)

    def __init__(self, value):
        self.value = value

#def key(group, name, required=False, valuetype=None, pattern=None):
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
#        k.required = required 
#        k.pattern = pattern
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

push_stack = 0

def newDict(value, group=None):
#    print (group)
    available = keys(group)

    d = {}
    for k, v in value.items():
#        print(available, k)
        try:
            available.remove(k)
        except ValueError:
            log.error("Key '"+k+"' not in '"+group+"' group")
        if isinstance(v, dict):
            d[k] = dictionary(k, group)(v)
        elif isinstance(v, list):
            d[k] = array(k, group)(v)
        elif isinstance(v, str):
            d[k] = key(k, group)(v)
        else:
            log.error("Key '"+k+"' has no subkeys!")

    return d



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
    key_table[group][name] = k
    return k

def dictionary(name, group=None):
    try:
        return key_table[group][name]
    except KeyError:
        pass

    def __init__(self, value):
        tf.isType(self.name, value, dict)
        self.value = newDict(value, name)

    def visit(self):
        global push_stack
        push_stack += 1

        for k, v in self.value.items():
#            print ("DICT", k, v)
            v.visit()

        push_stack -= 1

    k = key(name, group)
    k.visit = visit
    k.__init__ = __init__
    key_table[group][name] = k
    return k

def array(name, group=None):
    def __init__(self, value):
        tf.isType(self.name, value, list)

        self.value = []
        for v in value:
            self.value.append(dictionary(name, name)(v))

    def visit(self):
        global push_stack
        push_stack += 1
        for v in self.value:
            v.visit()
        global push_stack
        push_stack -= 1

    k = key(name, group)
    k.visit = visit
    k.__init__ = __init__
    key_table[group][name] = k
    return k


def collection(name, group=None):
    def __init__(self, value):
        tf.isType(self.name, value, dict)
        
        self.value = {}
        for k, v in value.items():
            print (v, name, k)
            self.value[k] = newDict(v, name)

    def visit(self):
        global push_stack
        push_stack += 1

        for k, v in self.value.items():
            push_stack += 1
            for subk, subv in v.items():
#                print (subk, subv)
                subv.visit()

            push_stack += -1
        push_stack += -1

    k = dictionary(name, group)
    k.visit = visit
    k.__init__ = __init__
    key_table[group][name] = k
    return k



#def getKey(group, k):
#    return key_table[group].get(k)
#
#def msgListKeys(group, keys, text):
#    output = ""
#
#    if len(keys):
#        output += "\n\n"+text+":"
#        for i in keys:
#            output += "\n- "+i
#
#    return output
#
#
#def getKeyDict(config, group):
#    newconfig = {}
#
#    notdefined = []
#    invalidkeys = []
#
#    for c in config.keys():
#        try:
#            newconfig[c] = getKey(group, c)(config[c])
#        except TypeError:
#            invalidkeys.append(c)
#
#    for i in keys(group):
#        if not i in newconfig.keys():
#            if key(group, i)().required:
#                notdefined.append(i)
#
#    if len(notdefined) or len(invalidkeys):
#        output = "Some '"+group+"' keys were not found or invalid!"
#        output += msgListKeys(group, notdefined,    "Not found")
#        output += msgListKeys(group, invalidkeys,   "Invalid keys")
#
#        log.error(output)
#
#    return newconfig
#
#def loadModule(config, key, modulename, package):
#    import PackthingImporter as importer
#    if key in config:
#
#        try:
#            importer.module(modulename, package)
#        except (KeyError, ImportError, TypeError):
#            if not modulename or modulename == None:
#                config.pop(key)
#            else:
#                log.error("No module '"+modulename+"' in '"+package.__name__+"'")
#
#    return config
#
#
#def mergeKeys(config, key, name):
#    if key in config:
#        try:
#            config[key][name].keys()
#        except KeyError:
#            log.warn("No "+key+"-specific key present: '"+name+"'")
#        except AttributeError:
#            log.warn("Empty "+key+"-specific key present: '"+name+"'")
#        except TypeError:
#            log.warn("Empty '"+key+"' key")
#        else:
#            for c in config[key][name].keys():
#                if c in config.keys():
#                    output = "'"+c+"' redefined as: "+str(config[key][name][c])+"\n"
#                    output += "First defined as: "+str(config[c])
#                    log.error(output)
#
#            config.update(config[key][name])
#
#        config.pop(key)
#
#    return config
#
