class Analyzer:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, val):
        self._total = val

obj = Analyzer(12)
print(obj.get_total())
obj.set_total(17)
print(obj.get_total())
