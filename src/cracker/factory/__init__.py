from typing import List, Tuple

from ..supported import NAMED_TYPE, Type
from ..parsers import Makefile, Npm, Justfile
from ..runners import Runner, Command, State


def RunnerFactory(target: str, runner: Type = Type.MAKEFILE) -> Type | None:
    """Factory Method for different runner types"""

    if runner == Type.Just:
        return Runner(
            command=Command(
                state=State.STOPPED,
                runner="just",
                args=["--summary"],
                target=target,
                process=None,
            )
        )
    elif runner == Type.MAKEFILE:
        return Runner(
            command=Command(
                state=State.STOPPED,
                runner="make",
                args=["--silent"],
                target=target,
                process=None,
            )
        )
    elif runner == Type.NPM:
        return Runner(
            command=Command(
                state=State.STOPPED,
                runner="npm",
                args=["run"],
                target=target,
                process=None,
            )
        )
    logger.warn(f"task runner type {runner} not found")
    return None


def ParserFactory(filename: str) -> Tuple[Type, List[str]]:

    parsers = {
        Type.MAKEFILE: Makefile.targets,
        Type.NPM: Npm.targets,
        Type.JUST: Justfile.targets,
    }
    type = NAMED_TYPE[filename]

    return (type, parsers[NAMED_TYPE[filename]](filename))
