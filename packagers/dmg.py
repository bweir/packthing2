import keyengine as kk

kk.dictionary("dmg",    "packager")

kk.info("background",   "dmg",      kk.PATH_REL)
kk.info("bundle",       "dmg",      kk.SLUG)

def tree():
    return {
        "ext": "dmg",
    }

