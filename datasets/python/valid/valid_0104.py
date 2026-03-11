class Calculator:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, m):
        self._x = m

obj = Calculator(8)
print(obj.get_x())
obj.set_x(11)
print(obj.get_x())
