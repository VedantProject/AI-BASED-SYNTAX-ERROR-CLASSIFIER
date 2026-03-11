class Calculator:
    def __init__(self, temp):
        self._temp = temp

    def get_temp(self):
        return self._temp

    def set_temp(self, n):
        self._temp = n

obj = Calculator(28)
print(obj.get_temp())
obj.set_temp(3)
print(obj.get_temp())
