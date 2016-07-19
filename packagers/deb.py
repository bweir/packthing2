import parsercore as core
import constants as cc

def parse(config):
    keylist = core.KeyList({
            "depends":      (core.optional,      str,    cc.RE_TEXT,        "declare Debian package dependencies",              "libftdi1"),
            "categories":   (core.optional,      str,    cc.RE_CATEGORIES,  "add your application to freedesktop categories",   "Development;IDE"),
            "section":      (core.optional,      str,    cc.RE_TEXT,        "add application to debian menus",                  "Applications/Editors"),
            "help2man":     (core.getStringList, list,   cc.RE_SLUG,        "generate man pages for binaris with help2man",     ""),
            })
    return core.getKeyList(config, keylist)

