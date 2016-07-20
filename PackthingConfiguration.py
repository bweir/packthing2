class Configuration(object):

    cfg_table = {}

    @classmethod
    def override(cls, key, value):
        cls.cfg_table[key] = value

    @classmethod
    def value(cls, key):
        return cls.cfg_table[key]

if 1:
    import platform

    p = Configuration
    p.cfg_table["platform"] = platform.system().lower().replace("darwin", "mac")
    p.cfg_table["arch"]     = platform.processor().replace("x86_64", "amd64")
    p.cfg_table["packager"] = None
