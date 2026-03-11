class Calculator:
    def __init__(self, temp):
        self._temp = temp

    def get_temp(self):
        return self._temp

    def set_temp(self, num):
        self._temp = num

obj = Calculator(48)
print(obj.get_temp())
obj.set_temp(20)
print(obj.get_temp())
