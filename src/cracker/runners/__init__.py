from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
import asyncio
import os
from . import IRunner, Command, State
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
    args: List[str]
    target: str
    process: asyncio.subprocess.Process | None


class IRunner(ABC):

    @abstractmethod
    def __init__(self, command: Command) -> None:
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args):
        pass


class Runner(IRunner):

    def __init__(self, command: Command) -> None:
        command.state = State.STOPPED
        self.command: Command = command

    async def __aenter__(self):
        self.command.process = await asyncio.create_subprocess_exec(
            self.command.runner,
            *self.command.args,
            self.command.target,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            stdin=asyncio.subprocess.PIPE,
            env=dict(os.environ, PYTHONUNBUFFERED="1"),
        )
        self.command.state = State.RUNNING
        return self.command.process

    async def __aexit__(self, *args):
        self.command.process.stdout._transport.close()
        self.command.process.stdin.close()
        await self.command.process.stdin.wait_closed()
        await self.command.process.wait()
