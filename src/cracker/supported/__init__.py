from typing import Dict
from enum import Enum, auto

NAMED: Dict[str, str] = {
    "Makefile": "make",
    "package.json": "npm",
    "justfile": "just",
}


class Type(Enum):
    MAKEFILE = auto()
    NPM = auto()
    JUST = auto()


NAMED_TYPE: Dict[str, Type] = {
    "Makefile": Type.MAKEFILE,
    "package.json": Type.NPM,
    "justfile": Type.JUST,
}
