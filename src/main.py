from typing import List
from main_window.mainwindow import MainWindow
from args.parser import Parser

import toml
from pathlib import Path

from supported import NAMED

parsed_toml = toml.load("pyproject.toml")["tool"]["poetry"]
VERSION = parsed_toml["version"]
DESCRIPTION = parsed_toml["description"]
NAME = parsed_toml["name"]
SUPPORTED = list(NAMED.keys())


def main() -> None:
    args = Parser.get_args()
    if args.version:
        print(VERSION)
        exit(0)
    files: List[str] = []
    print(args)
    if len(args.files) > 0:
        files += find_task_runners(args.files)
    else:
        files = find_task_runners()

    app = MainWindow(files)
    app.run()


def find_task_runners(files: List[str] = SUPPORTED) -> List[str]:
    return [file for file in files if Path(file).exists()]


if __name__ == "__main__":
    main()
