import util

def isMissingKeys(keylist):
    if len(_missingkeys):
        msg = "The following keys are missing from the packfile!\n"
        for k in _missingkeys:
            msg += "\n- %-16s %-50s (e.g. %s)" % (k,
                    keylist.description(k),
                    keylist.example(k))
        util.error(msg)

def isType(key, value, expected):
    if not type(value) is expected:
        util.error("Key '"+key+"' is of type '"+type(value).__name__+"';",
                   "expected '"+expected.__name__+"'.",
                   "(value: "+str(value)+")")

def isEmpty(key, value):
    if value == "" or value == None:
        util.error("'"+key+"' is defined but empty") 

def isMatch(key, value, pattern):
    regex = re.compile("^"+pattern+"$")
    try:
        if not regex.match(value):
            util.error(key+"' value '"+value+"' does not match pattern '"+pattern+"'")
    except TypeError:
        util.error("Invalid type for '"+key+"' value: "+str(value))

