import argparse


class Parser:
    def __init__(self):
        """Customer argument processing for Cracker"""

    @staticmethod
    def get_args() -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-v", "--version", help="display the version of ck", action="store_true"
        )
        parser.add_argument("files", nargs="*")
        args = parser.parse_args()
        return args
