class Calculator:
    def __init__(self, prod):
        self._prod = prod

    def get_prod(self):
        return self._prod

    def set_prod(self, temp):
        self._prod = temp

obj = Calculator(44)
print(obj.get_prod())
obj.set_prod(15)
print(obj.get_prod())
