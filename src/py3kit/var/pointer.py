class PointerVariable:
    def __init__(self, strings):
        self.string = string
        self.value = None
        self.update()
    def update(self):
        self.value = eval(self.string)
    def get(self):
        self.update()
        return self.value
    def set(self, string):
        self.string = string
    def __str__(self):
        return str(self.get())