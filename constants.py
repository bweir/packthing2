
RE_TEXT         = ".*"
RE_EMAIL        = "[^@]+@[^@]+\.[^@]+"
RE_URL          = "(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?"
RE_PATH_ABS     = "(/[^\\\]+)*"
RE_PATH_REL     = "[^\\\/]+"+RE_PATH_ABS
RE_SLUG         = "[a-z]*"
RE_CATEGORY     = "[a-z\-.]*"
RE_CATEGORIES   = "([a-zA-Z]+)(;[a-zA-Z]+)*"
RE_LICENSE      = "(MIT|GPLv3|BSD|Apache|GPLv2)"
RE_COPYRIGHT    = "[0-9]{4}(-[0-9]{4})?"


