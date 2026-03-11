class Tracker:
    def __init__(self, n):
        self._n = n

    def get_n(self):
        return self._n

    def set_n(self, item):
        self._n = item

obj = Tracker(21)
print(obj.get_n())
obj.set_n(4)
print(obj.get_n())
