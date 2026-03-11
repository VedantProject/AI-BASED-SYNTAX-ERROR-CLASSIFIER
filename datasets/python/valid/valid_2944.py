class Tracker:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, y):
        self._x = y

obj = Tracker(28)
print(obj.get_x())
obj.set_x(23)
print(obj.get_x())
