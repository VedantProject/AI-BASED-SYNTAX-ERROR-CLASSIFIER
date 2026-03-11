class Builder:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, count):
        self._total = count

obj = Builder(48)
print(obj.get_total())
obj.set_total(43)
print(obj.get_total())
