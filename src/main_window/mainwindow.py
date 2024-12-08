from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header

from main_window.taskgroup import TaskGroup


class MainWindow(App):
    """A textual app to manage your tasks"""

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "quit_app", "quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Main layout for the app window"""

        yield Header()
        yield Footer()
        yield HorizontalGroup(
            VerticalScroll(TaskGroup("makefile", ["rule1", "rule 2"]), id="tasks"),
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


if __name__ == "__main__":
    app = MainWindow()
    app.run()
