class Icon:
    def __init__(self, char):
        self.char: str = str(char)
        if len(self.char) != 1:
            from ..errors import DataOverflowError
            raise DataOverflowError("Icon objects can only hold objects that are of length 1 when converted to str")
    def __str__(self):
        return self.char
    def __eq__(self, other):
        return self.char == str(other)