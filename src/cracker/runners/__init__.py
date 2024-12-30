from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
import asyncio

from ..supported import Type


class State(Enum):
    STOPPED = auto()
    STARTED = auto()
    RUNNING = auto()
    KILL = auto()


@dataclass
class Target:
    type: Type
    target: str


@dataclass
class Command:
    state: State
    runner: str
    target: str
    process: asyncio.subprocess.Process | None


class IRunner(ABC):

    @abstractmethod
    def __init__(self, target: str) -> None:
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass


from .makefile import Makefile
from .npm import Npm
