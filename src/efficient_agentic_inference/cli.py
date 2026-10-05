"""Command dispatcher; inference and evaluation have independent entry points."""

import sys


def main() -> None:
    commands = ("predict", "evaluate", "snapshot")
    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        raise SystemExit("Usage: eai {predict|evaluate|snapshot} ...; v1 baseline was retired")
    command = sys.argv.pop(1)
    if command == "predict":
        from .predict import main as entry
    elif command == "evaluate":
        from .evaluation import main as entry
    else:
        from .snapshot import main as entry
    entry()
