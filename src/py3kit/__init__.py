class IncludeClass:
    def __init__(self, d):
        self.d = d
    def __call__(self, string: str):
        from importlib import import_module

        if "." in string:
            raise SyntaxError("py3kit.include uses '/' instead of '.'")

        module = import_module(f"py3kit.{string.replace("/", ".")}")

        if isinstance(self.d, dict):
            self.d |= module.__dict__

        return module
    def auto_globalize(self, d):
        self.d = d
    def fetch(self):
        from importlib.util import spec_from_file_location, module_from_spec
        from sys import argv
        from pathlib import Path

        path = Path(argv[1]) / "src" / "include"

        if not path.exists():
            from .errors import IncludeError
            raise IncludeError("src/include.py not found.")
        with path.open() as file:
            content = file.read()

        result = []

        for item in content.split("\n"):
            item = item.strip()
            if not item:
                continue
            result.append(self(item))
        return result

include = IncludeClass(None)