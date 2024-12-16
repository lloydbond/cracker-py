from typing import List, Dict

from textual import work
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
        self.richlog = RichLog(highlight=True, markup=False, max_lines=1_000)
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

    # @work(exclusive=True)
    # async def watch_output(self, new_output: List[str]) -> None:
    #     print("in watch")
    #     # self.richlog.clear()
    #     self.richlog.write("".join(self.output))

    # def on_mount(self):
    #     def watch_output() -> None:
    #         print("in watch output")
    #         print(self.output)
    #         self.richlog.write("".join(self.output))
    #         # self.richlog.write(f"{len(self.output)}")

    #     print("on mount for output")
    #     self.watch(self, "output", watch_output)

    def on_ready(self) -> None:
        self.richlog.write("stdout ready...\n\n")

    # async def on_rich_log_output(self, message: RichLogOutput) -> None:
    #     if message.update:
    #         self.richlog.write("".join(self.output))

    # @work(exclusive=True)
    async def on_task_stdout(self, message: Task.Stdout) -> None:
        print("hello world 2")
        # self.output.append(message.output)
        self.richlog.write(message.output)
        # self.post_message(self.RichLogOutput(True))
        # print(f"stdout extend output {len(self.output)}")
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
