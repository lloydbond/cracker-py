import argparse


class Parser:
    def __init__(self):
        """Customer argument processing for Cracker"""

    @staticmethod
    def get_args(
        VERSION: str, DESCRIPTION: str, NAME: str, SUPPORTED: str
    ) -> argparse.Namespace:
        parser = argparse.ArgumentParser(
            description=DESCRIPTION,
            prog=NAME,
            epilog=f"supported runners: [{'|'.join(SUPPORTED)}]\nversion: {VERSION}",
        )
        parser.add_argument("files", nargs="*")
        parser.add_argument(
            "--log",
            default="WARNING",
            help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
        )
        parser.add_argument(
            "-v", "--version", help="display the version of ck", action="store_true"
        )
        args = parser.parse_args()
        return args
