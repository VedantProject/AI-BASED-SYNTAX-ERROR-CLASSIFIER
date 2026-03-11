class Calculator:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, a):
        self._y = a

obj = Calculator(50)
print(obj.get_y())
obj.set_y(46)
print(obj.get_y())
