from typing import List
import asyncio

from textual import on, work
from textual.message import Message
from textual.widgets import Button

from factory import RunnerFactory
from runners import State
from supported import Type


class Task(Button):
    """A label with button action"""

    class Stdout(Message):
        """stdout pipe output update"""

        def __init__(self, output: List[str]) -> None:
            self.output: List[str] = output
            super().__init__()

    def __init__(self, name: str, type: Type = Type.MAKEFILE) -> None:
        print(f"create task-{name} type:{type}")
        self.target = name
        self.type: Type = type
        self.state = State.STOPPED
        super().__init__(name, id=f"task-{name.replace(':', '-')}", classes="idle")

    @work(thread=True, exclusive=True)
    async def update_async(self):
        async def wait_me(stdin):
            import signal

            while not self.state == State.STOPPED:
                await asyncio.sleep(0.05)
            try:
                stdin.write(signal.SIGKILL)
                await stdin.drain()
            except AssertionError:
                print(
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
                print(
                    "Task Runner process cancelled mid stream. It's okay we are handling it here."
                )

            except Exception as e:
                print(f"exception type is {type(e)}")

            return line

        async with RunnerFactory(self.target, self.type) as proc:
            self.state = State.STARTED
            cnt = 0
            waiter = asyncio.create_task(wait_me(proc.stdin), name="WAITER")
            buffer = asyncio.create_task(wait_buf(), name="BUFFER")
            reader = asyncio.create_task(yield_stdout(proc.stdout), name="STDOUT")
            lines: List[str] = []
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

            self.state = State.STOPPED
            if not waiter.done():
                waiter.cancel()
            if not buffer.done():
                buffer.cancel()
            if len(lines) > 0:
                self.app.post_message(self.Stdout(lines[:]))

    @on(Button.Pressed, "Task")
    async def task_pressed(self, event: Button.Pressed) -> None:
        """Task start"""

        assert event.button.id is not None
        task = event.button.id.partition("-")[-1]
        if self.state == State.STOPPED:
            self.update_async()
        else:
            self.state = State.STOPPED
            self.post_message(self.Stdout([f"stop task {task}"]))
