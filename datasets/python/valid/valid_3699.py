class Engine:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, val):
        self._x = val

obj = Engine(19)
print(obj.get_x())
obj.set_x(26)
print(obj.get_x())
