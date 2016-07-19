import yaml
import pprint
import util
import re

key_table = {}
defined_keys = {}

class re_pattern(object):
    slug = "[a-z]+"

class key_base(object):
    name = None
    pattern = None
    value = None
    valuetype = None
    required = None

    def __repr__(self):
        return "%s (%s)" % (self.name, self.pattern)

    def setValue(self, value):
        if not type(value) is self.valuetype:
            util.error("Key '"+self.name+"' is of type '"+type(value).__name__+"';",
                       "expected '"+self.valuetype.__name__+"'.",
                       "(value: "+str(value)+")")

        self.value = value


#    def before_checkout(self):
#        pass
#
#    def checkout(self):
#        pass
#
#    def after_checkout(self):
#        pass
#
#
#    def before_build(self):
#        pass
#
#    def build(self):
#        pass
#
#    def after_build(self):
#        pass
#
#
#    def before_package(self):
#        pass
#
#    def package(self):
#        pass
#
#    def after_package(self):
#        pass


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



key("name",         True)
key("package",      True)
key("org",          True)
key("url",          True)
key("maintainer",   True)
key("email",        True)
key("copyright",    True)
key("license",      True)
key("tagline",      True)
key("description",  True)
key("master",       True)

#key("target",       True)
#key("repos",        True)


key("help2man",     True,   str,    re_pattern.slug)

@method(key("help2man"))
def package(self):
    print "packaging help2man"

k = key("help2man")
print k
print dir(k)
k().package()

k().setValue("Chicken")




#def tokenize(program):
#    for number, operator in token_pat.findall(program):
#        if number:
#            yield literal_token(number)
#        elif operator == "+":
#            yield operator_add_token()
#        else:
#            raise SyntaxError("unknown operator")
#        yield end_token()
#

#def load(filename):
#    try:
#        return yaml.load(open(filename))
#    except IOError:
#        util.error("'"+self.repofile+"' not found; please specify a valid packthing file")
#
#def parse(filename):
#
#    config = load(filename)
#
#    for f in tokenize("1+ 4"):
#        print(f)
#
#    #pprint.pprint(config)
#    print(yaml.safe_dump(config))
#
#parse('packthing.yml')

