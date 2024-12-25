from typing import List, Dict


from textual import work
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import RichLog, Footer, Header
from textual.worker import Worker, get_current_worker

from main_window.taskgroup import TaskGroup, Task
from parsers.makefile import Makefile


class MainWindow(App):
    """A textual app to manage your tasks"""

    class RichLogOutput(Message):
        """update the richlog widget"""

        def __init__(self, update: bool) -> None:
            self.update: bool = update
            print("richlogoutput message")
            super().__init__()

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "app.quit", "quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    _targets: Dict[str, List[str]]
    output: reactive[List[str]] = reactive(["start", "fart\n", "mart\n"])

    def __init__(self, files: List[str]):
        """The main window layout. Provide a list of task runner files"""

        self._targets = {file: Makefile().targets(file) for file in files}
        super().__init__()

    def compose(self) -> ComposeResult:
        """Main layout for the app window"""
        richlog = RichLog(
            highlight=True,
            max_lines=1000,
            markup=False,
            id="richlog",
        )
        richlog.write("".join(self.output))

        yield Header()
        yield Footer()
        yield HorizontalGroup(
            VerticalScroll(
                *[TaskGroup(file, targets) for file, targets in self._targets.items()],
                id="tasks",
            ),
            VerticalScroll(
                richlog,
                id="stdoutput",
            ),
        )

    async def on_task_stdout(self, message: Task.Stdout) -> None:

        if len(message.output) <= 0:
            return

        self.update_output(message.output)

    @work(exclusive=True, thread=True, description="richlog_update")
    def update_output(self, output: List[str]) -> None:
        if len(output) <= 0:
            return
        richlog = self.query_one(RichLog)
        for line in output:
            richlog.write(line)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""

        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
