class Engine:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, diff):
        self._total = diff

obj = Engine(35)
print(obj.get_total())
obj.set_total(38)
print(obj.get_total())
