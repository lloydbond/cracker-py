from textual.widgets import Button


class ActionLabel(Button):
    """A label with button action"""

    def __init__(self, name: str):
        super().__init__(name, id=name)
