class Calculator:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, diff):
        self._m = diff

obj = Calculator(50)
print(obj.get_m())
obj.set_m(31)
print(obj.get_m())
