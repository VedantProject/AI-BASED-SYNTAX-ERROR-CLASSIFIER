class Calculator:
    def __init__(self, prod):
        self._prod = prod

    def get_prod(self):
        return self._prod

    def set_prod(self, total):
        self._prod = total

obj = Calculator(45)
print(obj.get_prod())
obj.set_prod(27)
print(obj.get_prod())
