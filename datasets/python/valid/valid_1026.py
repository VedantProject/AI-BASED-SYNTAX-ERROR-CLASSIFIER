class Scanner:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, res):
        self._x = res

obj = Scanner(48)
print(obj.get_x())
obj.set_x(36)
print(obj.get_x())
