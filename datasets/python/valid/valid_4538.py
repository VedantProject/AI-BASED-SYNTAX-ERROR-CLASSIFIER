class Scanner:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, acc):
        self._x = acc

obj = Scanner(12)
print(obj.get_x())
obj.set_x(32)
print(obj.get_x())
