class Tracker:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, z):
        self._total = z

obj = Tracker(49)
print(obj.get_total())
obj.set_total(34)
print(obj.get_total())
