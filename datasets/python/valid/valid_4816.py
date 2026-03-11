class Analyzer:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, res):
        self._total = res

obj = Analyzer(42)
print(obj.get_total())
obj.set_total(33)
print(obj.get_total())
