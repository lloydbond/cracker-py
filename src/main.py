from main_window.mainwindow import MainWindow
from args.parser import Parser

import toml

parsed_toml = toml.load("pyproject.toml")["tool"]["poetry"]
VERSION = parsed_toml["version"]
DESCRIPTION = parsed_toml["description"]
NAME = parsed_toml["name"]


def main():
    args = Parser.get_args()
    if args.version:
        print(VERSION)
        exit(0)

    if len(args.files) <= 0:
        exit(0)

    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
