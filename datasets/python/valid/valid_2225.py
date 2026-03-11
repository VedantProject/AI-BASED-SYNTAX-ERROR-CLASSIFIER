class Calculator:
    def __init__(self, n):
        self._n = n

    def get_n(self):
        return self._n

    def set_n(self, result):
        self._n = result

obj = Calculator(44)
print(obj.get_n())
obj.set_n(47)
print(obj.get_n())
