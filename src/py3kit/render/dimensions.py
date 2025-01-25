class Dimensions:
    def __init__(self, *dimensions):
        self.__dimensions = dimensions
    def __iter__(self):
        return iter(self.__dimensions)
    def get(self, n: int | None = None):
        try:
            return self.__dimensions if n is None else self.__dimensions[n - 1]
        except IndexError:
            from ..errors import OutOfBoundsError

            raise OutOfBoundsError(f"Dimensions.get() received an out-of-bounds dimension get request of dimension n. {n} ({n}D), while the Dimensions object has only {len(self.__dimensions)} dimensions ({len(self.__dimensions)}D   )")
    def get_type(self):
        return len(self.__dimensions)
    def as_str_letters(self):
        return ", ".join(list(self.as_dict_letters().keys()))
    def as_dict_letters(self):
        dimension_alphabet = [
            "",
            "x",
            "xy",
            "xyz",
            "wxyz"
        ]
        try:
            d: dict = {}
            for k, v in zip(
                dimension_alphabet[len(self.__dimensions)],
                self.__dimensions
            ):
                d[k] = v
            return d
        except IndexError:
            from ..errors import UnsupportedDimensionsError
            raise UnsupportedDimensionsError(f"Dimensions.as_dict_letters() only supports 0D, 1D, 2D, 3D, or 4D. It received a {len(self.__dimensions)}D object.")