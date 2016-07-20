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
key_stack = 0

class KeyBase(object):
    group = None
    name = None
    pattern = None
    value = None
    valuetype = None
    required = None

    def __repr__(self):
        return "((%s) %s: %s)" % (self.group, self.name, self.value)

    def setValue(self, value):
        tf.isType(self.name, value, self.valuetype)
        self.value = value

def key(group, name, required=False, valuetype=None, pattern=None):
    keys(group)

    try:
        k = key_table[group][name]
    except KeyError:
        class k(KeyBase):
            pass
        k.__name__ = name
        k.group = group
        k.name = name 
        k.required = required 
        k.valuetype = valuetype
        k.pattern = pattern
        k.value = None
        key_table[group][name] = k
    return k

def keys(group):
    try:
        g = key_table[group]
    except KeyError:
        g = {}
        key_table[group] = g
    return g

def method(k):
    assert issubclass(k, KeyBase)
    def bind(fn):
        setattr(k, fn.__name__, fn)
    return bind

def getKey(group, k):
    for i in key_table[group]:
        if k == i:
            return True
    return False

def msgListKeys(group, keys, text):
    output = ""

    if len(keys):
        output += "\n\n"+text+":"
        for i in keys:
            output += "\n- "+i

    return output


def getKeyDict(config, group):
    newconfig = {}

    notdefined = []
    invalidkeys = []

    for c in config:
        if getKey(group, c):
            newkey = key(group, c)()
            newkey.setValue(config[c])
            newconfig[c] = newkey
        else:
            invalidkeys.append(c)

    for i in keys(group):
        if not i in newconfig.keys():
            if key(group, i)().required:
                notdefined.append(i)

    if len(notdefined) or len(invalidkeys):
        output = "Some '"+group+"' keys were not found or invalid!"
        output += msgListKeys(group, notdefined,    "Not found")
        output += msgListKeys(group, invalidkeys,   "Invalid keys")

        log.error(output)

    return newconfig

def loadModule(config, key, modulename, package):
    import importer
    if key in config:

        try:
            importer.module(modulename, package)
        except (KeyError, ImportError, TypeError):
            if not modulename or modulename == None:
                config.pop(key)
            else:
                log.error("No module '"+modulename+"' in '"+package.__name__+"'")

    return config


def mergeKeys(config, key, name):
    if key in config:
        try:
            config[key][name].keys()
        except KeyError:
            log.warn("No "+key+"-specific key present: '"+name+"'")
        except AttributeError:
            log.warn("Empty "+key+"-specific key present: '"+name+"'")
        except TypeError:
            log.warn("Empty '"+key+"' key")
        else:
            for c in config[key][name].keys():
                if c in config.keys():
                    output = "'"+c+"' redefined as: "+str(config[key][name][c])+"\n"
                    output += "First defined as: "+str(config[c])
                    log.error(output)

            config.update(config[key][name])

        config.pop(key)

    return config

