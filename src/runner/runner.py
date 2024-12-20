from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
import asyncio
import psutil
import signal

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="stream2.log", encoding="utf-8", level=logging.DEBUG)


class Type(Enum):
    MAKEFILE = auto()


class State(Enum):
    STOPPED = auto()
    STARTED = auto()
    RUNNING = auto()


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

    async def __aexit__(self, *args):
        pass

    # @abstractmethod
    # async def start(self) -> None:
    #     pass

    # @abstractmethod
    # async def stop(self) -> int:
    #     pass

    # @property
    # @abstractmethod
    # def state(self) -> State:
    #     pass

    # @property
    # @abstractmethod
    # def stdout(self):
    #     pass

    # @abstractmethod
    # async def wait(self) -> int | None:
    #     pass


class Makefile(IRunner):

    def __init__(self, target: str) -> None:
        self.command: Command = Command(
            state=State.STOPPED, runner="make", target=target, process=None
        )

    async def __aenter__(self):
        import os

        print("with __enter__")
        print(f"{self.command.runner} {self.command.target}")
        self.command.process = await asyncio.create_subprocess_exec(
            self.command.runner,
            self.command.target,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            stdin=asyncio.subprocess.PIPE,
            env=dict(os.environ, PYTHONUNBUFFERED="1"),
        )
        self.command.state = State.RUNNING
        print(f"started {self.command.runner} {self.command.target}")
        return self.command.process

    async def __aexit__(self, *args):

        print(f"with __exit__ {self.command.process.returncode}")
        # self.target.process.stdin.write(signal.SIGTERM)
        if self.command.process.returncode is None:

            while psutil.pid_exists(self.command.process.pid):
                print("kill terminate wait")
                await asyncio.sleep(1.0)
                self.command.process.kill()

        retcode = await self.command.process.wait()
        print(f"stopped {self.command.runner} {self.command.target}")
        return retcode

    def cancel(self):
        if not self.command.process.returncode:
            print("kill terminate wait")
            self.command.process.stdin.write(signal.SIGTERM)


def Factory(target: str, runner: Type = Type.MAKEFILE):
    """Factory Method for different runner types"""

    runners = {
        Type.MAKEFILE: Makefile,
    }

    return runners[runner](target)
