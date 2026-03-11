class Calculator:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, data):
        self._total = data

obj = Calculator(38)
print(obj.get_total())
obj.set_total(21)
print(obj.get_total())
