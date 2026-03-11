class Analyzer:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, temp):
        self._x = temp

obj = Analyzer(13)
print(obj.get_x())
obj.set_x(38)
print(obj.get_x())
