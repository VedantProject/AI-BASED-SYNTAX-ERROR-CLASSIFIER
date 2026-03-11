class Builder:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, num):
        self._total = num

obj = Builder(20)
print(obj.get_total())
obj.set_total(26)
print(obj.get_total())
