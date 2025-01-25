class Variable:
    def __init__(self, value):
        self.value = value
    def get(self):
        return self.value
    def set(self, value):
        self.value = value
    def __str__(self):
        return str(self.get())