import util
import testfunctions as tf

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

class key_base(object):
    name = None
    pattern = None
    value = None
    valuetype = None
    required = None

    def __repr__(self):
#        return "%14s: %-100s (%s, %s)" % (self.name, self.value, self.valuetype.__name__, self.pattern)
        return "(%s: %s)" % (self.name, self.value)

    def setValue(self, value):
        tf.isType(self.name, value, self.valuetype)
        self.value = value

def key(name, required=False, valuetype=None, pattern=None):
    try:
        k = key_table[name]
    except KeyError:
        class k(key_base):
            pass
        k.__name__ = name
        k.name = name 
        k.required = required 
        k.valuetype = valuetype
        k.pattern = pattern
        k.value = None
        key_table[name] = k
    return k

def method(k):
    assert issubclass(k, key_base)
    def bind(fn):
        setattr(k, fn.__name__, fn)
    return bind

def getKey(k):
    for i in key_table:
        if k == i:
            return True
    return False

def msgListKeys(text, keys):
    output = ""

    if len(keys):
        output += "\n\n"+text+":"
        for i in keys:
            output += "\n- "+i

    return output


def getKeyDict(config):
    newconfig = {}

    notdefined = []
    invalidkeys = []

    for c in config:
        if getKey(c):
            newkey = key(c)()
            newkey.setValue(config[c])
            newconfig[c] = newkey
        else:
            invalidkeys.append(c)

    for i in key_table.keys():
        if not i in newconfig.keys():
            if key(i)().required:
                notdefined.append(i)

    if len(notdefined) or len(invalidkeys):
        output = "Some keys were not found or invalid!"
        output += msgListKeys("Not found", notdefined)
        output += msgListKeys("Invalid keys", invalidkeys)

        util.error(output)

    return newconfig


def mergeKeys(config, key, name):
    if key in config:
        try:
            config[key][name]
        except KeyError:
            util.note("No "+key+"-specific keys present")
        else:
            for c in config[key][name].keys():
                if c in config.keys():
                    output = "'"+c+"' redefined as: "+str(config[key][name][c])+"\n"
                    output += "First defined as: "+str(config[c])
                    util.error(output)
    
            config.update(config[key][name])

        config.pop(key)

    return config

