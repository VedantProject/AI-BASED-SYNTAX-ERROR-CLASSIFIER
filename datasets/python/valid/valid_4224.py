class Scanner:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, result):
        self._total = result

obj = Scanner(9)
print(obj.get_total())
obj.set_total(31)
print(obj.get_total())
