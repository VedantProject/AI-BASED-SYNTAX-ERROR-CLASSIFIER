class Engine:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, count):
        self._x = count

obj = Engine(19)
print(obj.get_x())
obj.set_x(2)
print(obj.get_x())
