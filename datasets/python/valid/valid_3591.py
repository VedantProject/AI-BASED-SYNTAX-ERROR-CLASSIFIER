class Scanner:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, z):
        self._total = z

obj = Scanner(17)
print(obj.get_total())
obj.set_total(28)
print(obj.get_total())
