class Tracker:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, count):
        self._size = count

obj = Tracker(46)
print(obj.get_size())
obj.set_size(5)
print(obj.get_size())
