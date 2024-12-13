from typing import List

import hat.peg


class Makefile:
    """A make file parser that uses Parsing Expression Grammar to find targets to run"""

    GRAMMAR = hat.peg.Grammar(
        r"""
        Rule <- Targets ':'!'=' Prerequisite* (';' Recipe)? 
        Targets <- Target (Target)*
        Target <- Spacing [_a-zA-Z]+ Spacing
        Prerequisites <- (Prerequisite)*
        Prerequisite <- Spacing [a-zA-Z_.]+ Spacing
        Recipe <- Spacing [a-zA-Z_.]+ Spacing

        Spacing    <- (Space / Comment)*
        Comment    <- '#' (!EndOfLine .)* EndOfLine
        Space      <- ' ' / '\t' / EndOfLine
        EndOfLine  <- '\r\n' / '\n' / '\r'
        EndOfFile  <- !.
    """,
        "Rule",
    )
    TRANSFORMS = {
        "Rule": lambda n, c: c[0],
        "Targets": lambda n, c: [target for target in c if target[0] != "_"],
        "Target": lambda n, c: "".join(c[1:-1]),
    }

    @staticmethod
    def targets(filename: str) -> List[str]:
        targets: List[str] = []
        with open(filename, "r") as file:
            for line in file.readlines():
                line = line.strip()
                if len(line) <= 0:
                    continue
                try:
                    ast = Makefile.GRAMMAR.parse(
                        line,
                    )
                    result = hat.peg.walk_ast(ast, Makefile.TRANSFORMS)
                    targets += result
                except Exception:
                    continue
        return targets


if __name__ == "__main__":
    print(Makefile.targets("Makefile.tst"))
