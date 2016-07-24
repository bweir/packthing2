import keyengine as kk
import PackthingConfiguration as cfg

kk.dictionary("mac",    "platform")

kk.info("category",     "mac",    "[a-zA-Z-]+(\\.[a-zA-Z-]+)*",    True)

def setup():
    cfg.allow("packager",   ["dmg"])
