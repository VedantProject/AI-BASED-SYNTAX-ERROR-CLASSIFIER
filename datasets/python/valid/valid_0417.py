class Builder:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, z):
        self._size = z

obj = Builder(43)
print(obj.get_size())
obj.set_size(31)
print(obj.get_size())
