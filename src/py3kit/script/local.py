import os
from sys import argv, executable
from pathlib import Path
from subprocess import run

class LocalScript:
    def __init__(self, name, **dependencies):
        self.name = name
        self.dependencies = dependencies
        self.path = Path(argv[1]) / "scripts" / name

        if not self.path.is_file():
            raise FileNotFoundError(f"Script {self.name} not found.")
    def execute(self):
        run([executable, self.path])
    def to_class(self):
        with self.path.open() as file:
            content = file.read()
            if not content.strip():
                print(rf"/!\ EMPTY SCRIPT WARNING: {self.name}")
            text = f"""
class {self.name}:
    {"\n    ".join((content.strip() or "...").split("\n"))}
            """
            globals_call = globals()
            globals_call |= self.dependencies
            exec(text)
        return locals()[self.name]
    def apply(self, cls):
        return type(cls.__name__, (cls,), dict(self.to_class().__dict__))
    def read(self):
        with self.path.open() as file:
            return file.read()