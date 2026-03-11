class Tracker:
    def __init__(self, a):
        self._a = a

    def get_a(self):
        return self._a

    def set_a(self, size):
        self._a = size

obj = Tracker(24)
print(obj.get_a())
obj.set_a(5)
print(obj.get_a())
