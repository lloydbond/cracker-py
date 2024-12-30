import logging
from typing import List
from importlib.metadata import version
from .supported import NAMED
from .mainwindow import MainWindow
from .args.parser import Parser
from textual.logging import TextualHandler


# import toml
from pathlib import Path

logger = logging.getLogger(__name__)
# parsed_toml3 = toml.load("pyproject.toml")["tool"]["poetry"]
# VERSION = parsed_toml3["version"]
# DESCRIPTION = parsed_toml3["description"]
# NAME = parsed_toml3["name"]
VERSION = version
DESCRIPTION = "A task runner"
NAME = "cracker"
SUPPORTED = list(NAMED.keys())


def main() -> None:
    args = Parser.get_args(VERSION, DESCRIPTION, NAME, SUPPORTED)
    if args.version:
        print(VERSION)
        exit(0)
    files: List[str] = []
    log_level = "NOTSET"
    if args.log and args.log.upper() in [
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]:
        log_level = args.log.upper()

    logging.basicConfig(
        encoding="utf-8",
        level=(args.log.upper()),
        handlers=[TextualHandler()],
    )
    if len(args.files) > 0:
        logger.debug(args.files)
        files += find_task_runners(args.files)
    else:
        files = find_task_runners()

    app = MainWindow(files)
    app.run()
    logger.debug(f"{NAME} exited")


def find_task_runners(files: List[str] = SUPPORTED) -> List[str]:
    return [file for file in files if Path(file).exists()]


if __name__ == "__main__":
    main()
