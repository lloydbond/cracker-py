import asyncio
import os
from runners import Command, IRunner, State


class Npm(IRunner):

    def __init__(self, target: str) -> None:
        self.command: Command = Command(
            state=State.STOPPED, runner="npm", target=target, process=None
        )

    async def __aenter__(self):
        self.command.process = await asyncio.create_subprocess_exec(
            self.command.runner,
            "run",
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
