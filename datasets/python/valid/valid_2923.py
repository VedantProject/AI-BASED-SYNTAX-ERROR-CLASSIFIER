class Builder:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, x):
        self._size = x

obj = Builder(15)
print(obj.get_size())
obj.set_size(16)
print(obj.get_size())
