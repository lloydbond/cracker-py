from typing import List, Tuple
from supported import NAMED_TYPE, Type

from parsers import Makefile as pMakefile, Npm as pNpm
from runners import Makefile as rMakefile, Npm as rNpm


def RunnerFactory(target: str, runner: Type = Type.MAKEFILE):
    """Factory Method for different runner types"""

    runners = {
        Type.MAKEFILE: rMakefile,
        Type.NPM: rNpm,
    }

    return runners[runner](target)


def ParserFactory(filename: str) -> Tuple[Type, List[str]]:

    parsers = {
        Type.MAKEFILE: pMakefile.targets,
        Type.NPM: pNpm.targets,
    }
    type = NAMED_TYPE[filename]

    return (type, parsers[NAMED_TYPE[filename]](filename))
