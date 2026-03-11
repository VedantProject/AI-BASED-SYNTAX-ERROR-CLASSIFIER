class Tracker:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, res):
        self._count = res

obj = Tracker(36)
print(obj.get_count())
obj.set_count(4)
print(obj.get_count())
