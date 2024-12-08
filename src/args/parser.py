import argparse


class Parser:
    def __init__(self):
        """Customer argument processing for Cracker"""

    def get_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v", "--version", help="display the version of ck", action="store_true"
        )
        parser.add_argument("file", nargs="*")
        args = parser.parse_args()
        return args
