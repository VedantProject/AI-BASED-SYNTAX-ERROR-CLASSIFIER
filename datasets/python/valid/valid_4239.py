class Scanner:
    def __init__(self, val):
        self._val = val

    def get_val(self):
        return self._val

    def set_val(self, size):
        self._val = size

obj = Scanner(19)
print(obj.get_val())
obj.set_val(42)
print(obj.get_val())
