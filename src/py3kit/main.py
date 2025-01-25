from sys import argv, executable
from pathlib import Path
from subprocess import run
from os import getcwd

def main(**kwargs):
    args = argv[1:]

    if not args:
        args.append(".")

    here = Path(getcwd()) / args[0]
    src = here / "src"
    entry = src / "main.py"

    try:
        return run([executable, str(entry), here] + args, **kwargs)
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        print("<program finished>")