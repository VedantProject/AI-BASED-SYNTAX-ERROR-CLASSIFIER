class Tracker:
    def __init__(self, b):
        self._b = b

    def get_b(self):
        return self._b

    def set_b(self, size):
        self._b = size

obj = Tracker(34)
print(obj.get_b())
obj.set_b(33)
print(obj.get_b())
