from typing import List

from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.message import Message
from textual.widgets import ListItem, ListView, Button

from runner.runner import IRunner, Factory, State, Type


class ActionLabel(Button):
    """A label with button action"""

    def __init__(self, name: str):
        super().__init__(name)


class Task(Button):
    """A label with button action"""

    class Stdout(Message):
        """stdout pipe output update"""

        def __init__(self, output: str) -> None:
            self.output = output
            super().__init__()

    def __init__(self, name: str) -> None:
        print(f"create task-{name}")
        self.t: IRunner = Factory(name, Type.MAKEFILE)
        super().__init__(name, id=f"task-{name}")

    async def update_output(self) -> None:
        line = ""
        for char in self.t.stdout:
            if self.t.state() == State.STOPPED:
                break

            if char == "\n":
                self.post_message(self.Stdout(line))
                line = ""
                continue
            line += char
        self.post_message(self.Stdout(line))

    @on(Button.Pressed, "Task")
    def task_pressed(self, event: Button.Pressed) -> None:
        """Task start"""

        assert event.button.id is not None
        task = event.button.id.partition("-")[-1]
        if self.t.state() == State.STOPPED:
            self.t.start()
            print(f"start task {task}")
            self.run_worker(
                self.update_output(), start=True, thread=True, exclusive=True
            )
        else:
            print(f"stop task {task}")
            self.t.stop()
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

    def start_pressed(self) -> None:
        """Start task"""
