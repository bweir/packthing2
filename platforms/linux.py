import keyengine as kk
import PackthingConfiguration as cfg

kk.dictionary("linux",      "platform")

kk.info("categories",       "linux",    "[a-zA-Z]+(;[a-zA-Z]+)*",    True)
kk.info("section",          "linux",    "[a-zA-Z]+(/[a-zA-Z]+)*",    True)
kk.infoList("help2man",     "linux",    kk.SLUG)

def platform():
    return {
        "ext":
        {
            "bin": "",
            "lib": "so"
        },
        "prefix":
        {
            "lib": "lib",
        },
        "path":
        {
            "bin": "bin",
            "lib": "lib",
            "share": "share/propelleride",
        }
    }

def setup():
    cfg.allow("packager",   ["deb"])
