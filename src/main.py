from typing import List
from main_window.mainwindow import MainWindow
from args.parser import Parser

import toml

parsed_toml = toml.load("pyproject.toml")["tool"]["poetry"]
VERSION = parsed_toml["version"]
DESCRIPTION = parsed_toml["description"]
NAME = parsed_toml["name"]


def main() -> None:
    args = Parser.get_args()
    if args.version:
        print(VERSION)
        exit(0)
    files: List[str] = args.files
    if len(files) <= 0:
        files += find_task_runners()

    app = MainWindow(files)
    app.run()


if __name__ == "__main__":
    main()


def find_task_runners() -> List[str]:
    return ["Makefile"]
