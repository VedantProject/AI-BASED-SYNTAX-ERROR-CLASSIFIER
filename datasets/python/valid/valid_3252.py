class Manager:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, val):
        self._size = val

obj = Manager(42)
print(obj.get_size())
obj.set_size(42)
print(obj.get_size())
