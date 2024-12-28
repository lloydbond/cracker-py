from typing import List
from json import load


class Npm:
    """A package.json parser"""

    @staticmethod
    def targets(filename: str) -> List[str]:
        with open(filename, "r") as file:
            result = load(file)
            if "scripts" in result:
                return list(result["scripts"].keys())

        return []


if __name__ == "__main__":
    print(Npm.targets("package.json"))
