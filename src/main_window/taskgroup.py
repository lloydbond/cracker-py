from typing import List
import asyncio

from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup
from textual.message import Message
from textual.widgets import ListItem, ListView, Button
from textual.worker import Worker

from runner.runner import Factory, State, Type


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
        self.target = name
        self.state = State.STOPPED
        # self.proc: IRunner = Factory(name, Type.MAKEFILE)
        super().__init__(name, id=f"task-{name}")

    async def update_async(self):
        import logging

        logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename="stream2.log", encoding="utf-8", level=logging.DEBUG
        )

        async def wait_me(stdin):
            import signal

            while not self.state == State.STOPPED:
                await asyncio.sleep(0.05)
            stdin.write(signal.SIGKILL)
            await stdin.drain()
            return b""

        async def yield_stdout(stdout):
            line = ""
            try:
                line = await stdout.readline()
            except Exception as e:
                print(f"exception type is {type(e)}")
                print("Task Runner process cancelled mid stream.")

            return line

        async with Factory(self.target, Type.MAKEFILE) as proc:
            self.state = State.STARTED
            waiter = asyncio.create_task(wait_me(proc.stdin), name="WAITER")
            r = None
            while True:
                r = asyncio.create_task(yield_stdout(proc.stdout), name="STDOUT")
                done, _ = await asyncio.wait(
                    [r, waiter],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                for task in done:
                    if task.exception() is not None:
                        data = b""
                        r.cancel()
                        break

                    data = await task
                if data == b"":
                    logger.debug("end of stream")
                    break
                logger.debug(self.state)
                print(f"data: {data}")
                line = data.decode().rstrip()
                self.app.post_message(self.Stdout(line))
                logger.debug(line)
            self.state = State.STOPPED
            if not waiter.done():
                waiter.cancel()

    async def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        self.log(event)

    @on(Button.Pressed, "Task")
    async def task_pressed(self, event: Button.Pressed) -> None:
        """Task start"""

        assert event.button.id is not None
        task = event.button.id.partition("-")[-1]
        if self.state == State.STOPPED:
            print(f"start task {task}")
            self.wok = self.app.run_worker(
                self.update_async,
                name=f"task {task}",
                group=self.target,
                start=True,
                thread=True,
                exclusive=True,
            )
            print(f"worker started: {self.wok.is_running}")
        else:
            print(f"stop task {task}")
            self.state = State.STOPPED
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
