class Manager:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, acc):
        self._x = acc

obj = Manager(12)
print(obj.get_x())
obj.set_x(49)
print(obj.get_x())
