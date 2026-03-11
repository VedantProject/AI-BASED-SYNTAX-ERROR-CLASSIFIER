class Calculator:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, val):
        self._y = val

obj = Calculator(15)
print(obj.get_y())
obj.set_y(34)
print(obj.get_y())
