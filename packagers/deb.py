import keyengine as kk

kk.dictionary("deb",    "packager")

kk.infoList("depends",  "deb",      "[a-zA-Z0-9\\-]+")

def tree():
    return {
        "ext": "deb",
    }

