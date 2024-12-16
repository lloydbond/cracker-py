from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto

from subprocess import Popen, PIPE


class State(Enum):
    STOPPED = auto()
    STARTED = auto()
    RUNNING = auto()


@dataclass
class Target:
    state: State
    runner: str
    target: str
    process: Popen | None


class IRunner(ABC):

    @abstractmethod
    def __init__(self, target: str) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @abstractmethod
    def state(self) -> State:
        pass

    @property
    @abstractmethod
    def stdout(self):
        pass


class Type(Enum):
    MAKEFILE = auto()


class Makefile(IRunner):
    def __init__(self, target: str) -> None:
        self.target: Target = Target(
            state=State.STOPPED, runner="make", target=target, process=None
        )

    def start(self) -> None:
        if self.target.state == State.STOPPED:
            self.target.process = Popen(
                [self.target.runner, self.target.target],
                bufsize=1,
                stdout=PIPE,
                # stderr=STDOUT,
                text=True,
            )
            self.target.state = State.STARTED
            self._stdout = self.target.process.stdout
            self.target.state = State.RUNNING
        print(f"started {self.target.runner} {self.target.target}")

    def stop(self) -> None:
        self.target.state = State.STOPPED
        if self._stdout is not None:
            self._stdout.close()
        print(f"stopped {self.target.runner} {self.target.target}")

    def state(self) -> State:
        return self.target.state

    @property
    def stdout(self):
        return self._stdout


def Factory(target: str, runner: Type = Type.MAKEFILE):
    """Factory Method for different runner types"""

    runners = {
        Type.MAKEFILE: Makefile,
    }

    return runners[runner](target)
