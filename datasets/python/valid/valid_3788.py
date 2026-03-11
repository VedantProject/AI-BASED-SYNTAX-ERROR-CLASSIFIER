class Manager:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, x):
        self._size = x

obj = Manager(41)
print(obj.get_size())
obj.set_size(34)
print(obj.get_size())
