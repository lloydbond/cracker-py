from typing import List

from textual import on, work
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.message import Message
from textual.widgets import ListItem, ListView, Button
from textual.worker import Worker

from runner.runner import IRunner, Factory, State, Type
import asyncio


class ActionLabel(Button):
    """A label with button action"""

    def __init__(self, name: str):
        super().__init__(name)


class Task(Button):
    """A label with button action"""

    class Stdout(Message):
        """stdout pipe output update"""

        def __init__(self, output: str) -> None:
            self.output: str = output
            super().__init__()

    def __init__(self, name: str) -> None:
        print(f"create task-{name}")
        self.t: IRunner = Factory(name, Type.MAKEFILE)
        super().__init__(name, id=f"task-{name}")

    async def update_output(self) -> None:
        print("in run_worker update_output()")
        cnt = 1
        for line in iter(self.t.stdout.readline, ""):
            self.post_message(self.Stdout(line[:-1]))
            if cnt % 10 == 0:
                print("Hello world 0")
            if self.t.state() == State.STOPPED or cnt > 100_000:
                break
            cnt += 1
        print("hello world 1")

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        print("worker state changed")
        self.log(event)

    @on(Button.Pressed, "Task")
    async def task_pressed(self, event: Button.Pressed) -> None:
        """Task start"""

        assert event.button.id is not None
        task = event.button.id.partition("-")[-1]
        if self.t.state() == State.STOPPED:
            self.t.start()
            print(f"start task {task}")
            self.wok = self.run_worker(
                self.update_output(),
                name=f"task {task}",
                group="makefile",
                start=True,
                thread=True,
                exclusive=True,
            )
            print(f"worker started: {self.wok.is_running}")
        else:
            print(f"stop task {task}")
            self.t.stop()
            self.wok.cancel()
            self.post_message(self.Stdout(f"stop task {task}"))


class TaskGroup(HorizontalGroup):
    """A ListView of rule targets for each task runner type"""

    name: str = ""
    targets: List[ListItem] = []

    def __init__(self, name: str, targets: List[str], id: str | None = None):
        """name of the taskrunner and a list of the targets to run"""
        self.name = name
        self.targets = [ListItem(Task(target)) for target in targets]
        super().__init__()

    def compose(self) -> ComposeResult:
        # yield Label(self.name)
        yield ActionLabel(self.name)
        yield ListView(*self.targets)
