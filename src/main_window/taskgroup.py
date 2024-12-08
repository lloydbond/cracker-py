from typing import List

from textual.app import ComposeResult
from textual.containers import HorizontalGroup, Widget
from textual.widgets import Label, ListItem, ListView


class TaskGroup(HorizontalGroup):
    """A ListView of rule targets for each task runner type"""

    name: str = ""
    targets: List[ListItem] = []

    def __init__(self, name: str, targets: List[str], id: str | None = None):
        """name of the taskrunner and a list of the targets to run"""
        self.name = name
        self.targets = [ListItem(Label(target, id="target")) for target in targets]
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.name)
        yield ListView(*self.targets)
