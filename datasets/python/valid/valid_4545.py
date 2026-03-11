class Engine:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, prod):
        self._x = prod

obj = Engine(31)
print(obj.get_x())
obj.set_x(5)
print(obj.get_x())
