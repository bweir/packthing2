import keyengine as kk
import PackthingConfiguration as cfg

def tree():
    return {
        "ext":
        {
            "bin": "exe",
            "lib": "dll",
        },
        "prefix":
        {
            "lib": "",
        },
        "path":
        {
            "bin": "",
            "lib": "",
            "share": "",
        }
    }

def setup():
    cfg.allow("packager",   ["inno"])

