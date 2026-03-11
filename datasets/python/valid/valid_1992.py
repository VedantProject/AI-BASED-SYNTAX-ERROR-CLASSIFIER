class Tracker:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, result):
        self._size = result

obj = Tracker(31)
print(obj.get_size())
obj.set_size(21)
print(obj.get_size())
