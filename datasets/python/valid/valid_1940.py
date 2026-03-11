class Worker:
    def __init__(self, total):
        self._total = total

    def get_total(self):
        return self._total

    def set_total(self, m):
        self._total = m

obj = Worker(36)
print(obj.get_total())
obj.set_total(38)
print(obj.get_total())
