class Tracker:
    def __init__(self, n):
        self._n = n

    def get_n(self):
        return self._n

    def set_n(self, count):
        self._n = count

obj = Tracker(14)
print(obj.get_n())
obj.set_n(9)
print(obj.get_n())
