from enum import Enum, auto

NAMED = {
    "Makefile": "make",
    "package.json": "npm",
}


class Type(Enum):
    MAKEFILE = auto()
    NPM = auto()


NAMED_TYPE = {
    "Makefile": Type.MAKEFILE,
    "package.json": Type.NPM,
}
