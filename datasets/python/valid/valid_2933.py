class Analyzer:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, a):
        self._total = a

obj = Analyzer(34)
print(obj.get_total())
obj.set_total(47)
print(obj.get_total())
