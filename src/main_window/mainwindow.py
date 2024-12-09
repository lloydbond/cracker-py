from typing import List, Dict

from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header

from main_window.taskgroup import TaskGroup
from parsers.makefile import Makefile


class MainWindow(App):
    """A textual app to manage your tasks"""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "quit_app", "quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    _targets: Dict[str, List[str]]

    def __init__(self, files: List[str]):
        """The main window layout. Provide a list of task runner files"""

        self._targets = {file: Makefile().targets(file) for file in files}
        super().__init__()

    def compose(self) -> ComposeResult:
        """Main layout for the app window"""

        yield Header()
        yield Footer()
        yield HorizontalGroup(
            VerticalScroll(
                *[TaskGroup(file, targets) for file, targets in self._targets.items()],
                id="tasks"
            ),
            VerticalScroll(id="stdoutput"),
        )

    def action_quit_app(self) -> None:
        """Quit the app"""

        self.app.exit()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""

        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


# if __name__ == "__main__":
#     app = MainWindow()
#     app.run()
