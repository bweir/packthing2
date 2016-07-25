import keyengine as kk
import PackthingConfiguration as cfg

kk.dictionary("mac",    "platform")

kk.info("category",     "mac",    "[a-zA-Z-]+(\\.[a-zA-Z-]+)*",    True)

def tree():
    return {
        "ext":
        {
            "bin": "",
            "lib": "dylib"
        },
        "prefix":
        {
            "lib": "",
        },
        "path":
        {
            "bin": "MacOS",
            "lib": "MacOS",
            "share": "Resources",
        }
    }

def setup():
    cfg.allow("packager",   ["dmg"])
