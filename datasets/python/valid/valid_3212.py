class Tracker:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, b):
        self._total = b

obj = Tracker(19)
print(obj.get_total())
obj.set_total(34)
print(obj.get_total())
