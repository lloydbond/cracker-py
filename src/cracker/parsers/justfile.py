from typing import List

from subprocess import Popen, PIPE


class Justfile:
    """A just file parser that uses Parsing Expression Grammar to find targets to run"""

    @staticmethod
    def targets(filename: str) -> List[str]:
        targets: List[str] = []
        with Popen(["just", "--justfile", filename, "--summary"], stdout=PIPE) as proc:
            targets = [
                target.strip()
                for target in proc.stdout.readlines()[0].decode().split(" ")
            ]
        return targets


if __name__ == "__main__":
    print(Justfile.targets("justfile"))
