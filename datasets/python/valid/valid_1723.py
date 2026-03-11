class Calculator:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, m):
        self._count = m

obj = Calculator(43)
print(obj.get_count())
obj.set_count(24)
print(obj.get_count())
