from typing import List, Dict, Tuple


from textual import work, on
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.message import Message
from textual.widgets import RichLog, Footer, Header, Button, ListView, ListItem


from .task import Task
from .actionlabel import ActionLabel
from ..factory import ParserFactory
from ..supported import NAMED, Type


class MainWindow(App):
    """A textual app to manage your tasks"""

    class RichLogOutput(Message):
        """update the richlog widget"""

        def __init__(self, update: bool) -> None:
            self.update: bool = update
            super().__init__()

    CSS_PATH = "app.tcss"
    BINDINGS = [
        ("q", "app.quit", "quit"),
        ("d", "toggle_dark", "Toggle dark mode"),
    ]
    _targets: Dict[str, Tuple[Type, List[str]]]

    def __init__(self, files: List[str]):
        """The main window layout. Provide a list of task runner files"""

        self._targets = {NAMED[file]: ParserFactory(file) for file in files}
        super().__init__()

    def compose(self) -> ComposeResult:
        """Main layout for the app window"""
        richlog = RichLog(
            highlight=True,
            max_lines=1000,
            markup=False,
            id="richlog",
        )
        richlog.write("start your task ...")
        runner_listview = ListView(
            *[ListItem(ActionLabel(name)) for name in self._targets.keys()]
        )

        yield Header()
        yield Footer()
        yield HorizontalGroup(
            VerticalScroll(runner_listview, id="runners"),
            VerticalScroll(ListView(), id="targets"),
            VerticalScroll(richlog, id="stdoutput"),
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

    @on(Button.Pressed, "ActionLabel")
    async def label_pressed(self, event: Button.Pressed) -> None:
        """Runner label pressed"""

        print("action label pressed")
        assert event.button.id is not None
        print(event.button.id)
        print(
            *[
                (target, self._targets[event.button.id][0])
                for target in self._targets[event.button.id][1]
            ]
        )
        list_view = self.query_one("#targets").query_one(ListView)
        list_view.clear()
        print(self._targets[event.button.id][0])
        print(self._targets[event.button.id][1])
        list_view.extend(
            [
                ListItem(Task(target, self._targets[event.button.id][0]))
                for target in self._targets[event.button.id][1]
            ]
        )
