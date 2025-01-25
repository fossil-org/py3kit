class ScriptHandler:
    def __init__(self, cls):
        self.cls = cls
    def new(self, script, obj, **dependencies):
        return self.cls(script, this=obj, **dependencies).apply(obj)