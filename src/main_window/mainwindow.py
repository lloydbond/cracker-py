from typing import List, Dict

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import RichLog, Footer, Header

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
    output: reactive[List[str]] = reactive([], always_update=True)
    richlog: RichLog

    def __init__(self, files: List[str]):
        """The main window layout. Provide a list of task runner files"""

        self._targets = {file: Makefile().targets(file) for file in files}
        self.richlog = RichLog(
            id="richlog", highlight=True, markup=False, max_lines=1_000
        )
        super().__init__()

    def compose(self) -> ComposeResult:
        """Main layout for the app window"""

        yield Header()
        yield Footer()
        yield HorizontalGroup(
            VerticalScroll(
                *[TaskGroup(file, targets) for file, targets in self._targets.items()],
                id="tasks",
            ),
            VerticalScroll(self.richlog, id="stdoutput"),
        )

    def on_ready(self) -> None:
        self.richlog.write("stdout ready...\n\n")

    async def on_task_stdout(self, message: Task.Stdout) -> None:
        self.richlog.write(message.output)
        if len(self.output) > 1_000_000:
            print("over 1 million, needs trim")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""

        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


# if __name__ == "__main__":
#     app = MainWindow()
#     app.run()
