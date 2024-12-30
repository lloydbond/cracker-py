import logging
from typing import List
import asyncio

from textual import on, work
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Button
from textual.logging import TextualHandler

from ..factory import RunnerFactory
from ..runners import State
from ..supported import Type

logger = logging.getLogger(__name__)
# logging.basicConfig(
#     encoding="utf-8",
#     level=logging.INFO,
#     handlers=[TextualHandler()],
# )


class Task(Button):
    """A label with button action"""

    class Stdout(Message):
        """stdout pipe output update"""

        def __init__(self, output: List[str]) -> None:
            self.output: List[str] = output
            super().__init__()

    state: State = reactive(State.STOPPED)

    def __init__(self, name: str, type: Type = Type.MAKEFILE) -> None:
        logger.debug(f"create task-{name} type:{type}")
        self.target = name
        self.type: Type = type
        super().__init__(name, id=f"task-{name.replace(':', '-')}")

    @work(thread=True, exclusive=True)
    async def update_async(self):
        self.state = State.STARTED

        async def wait_me(stdin):
            import signal

            while not self.state == State.KILL:
                await asyncio.sleep(0.05)
            try:
                stdin.write(signal.SIGKILL)
                await stdin.drain()
            except AssertionError:
                logger.debug(
                    "Unable to send kill signal to the running child process. Did someone manually kill it?"
                )
            return b""

        async def wait_buf():
            await asyncio.sleep(0.2)

        async def yield_stdout(stdout) -> str:
            line = ""
            try:
                line = await stdout.readline()
            except RuntimeError:
                logger.debug(
                    "Task Runner process cancelled mid stream. It's okay we are handling it here."
                )

            except Exception as e:
                logger.debug(
                    f"Wow, something crazy and unexpected just happened, please report it as a bug\n {e}"
                )

            return line

        async with RunnerFactory(self.target, self.type) as proc:
            cnt = 0
            waiter = asyncio.create_task(wait_me(proc.stdin), name="WAITER")
            buffer = asyncio.create_task(wait_buf(), name="BUFFER")
            reader = asyncio.create_task(yield_stdout(proc.stdout), name="STDOUT")
            lines: List[str] = []
            self.state = State.RUNNING
            while True:

                done, _ = await asyncio.wait(
                    [
                        buffer,
                        waiter,
                        reader,
                    ],
                    return_when=asyncio.FIRST_COMPLETED,
                )
                task = done.pop()
                if task.get_name() == "BUFFER":
                    if len(lines) > 0:
                        self.app.post_message(self.Stdout(lines[:]))
                        lines.clear()
                        cnt += 1
                    buffer = asyncio.create_task(wait_buf(), name="BUFFER")
                    continue

                if task.exception() is not None:
                    reader.cancel()
                    break

                data = await task
                if data == b"":
                    break
                lines.append(data.decode().rstrip())
                reader = asyncio.create_task(yield_stdout(proc.stdout), name="STDOUT")

            if not waiter.done():
                waiter.cancel()
            if not buffer.done():
                buffer.cancel()
            if len(lines) > 0:
                self.app.post_message(self.Stdout(lines[:]))
            self.state = State.STOPPED

    async def watch_state(self, old_state: State, new_state: State) -> None:
        logger.debug(f"state: {old_state} -> {new_state}")
        m = {
            State.RUNNING: "stop",
            State.KILL: "stopping",
            State.STARTED: "starting",
            State.STOPPED: "idle",
        }
        self.remove_class(m[old_state])
        self.add_class(m[new_state])

    @on(Button.Pressed, "Task")
    async def task_pressed(self, event: Button.Pressed) -> None:
        """Task start"""

        assert event.button.id is not None
        task = event.button.id.partition("-")[-1]
        if self.state == State.STOPPED:
            self.update_async()
        else:
            self.state = State.KILL
            self.post_message(self.Stdout([f"stop task {task}"]))
