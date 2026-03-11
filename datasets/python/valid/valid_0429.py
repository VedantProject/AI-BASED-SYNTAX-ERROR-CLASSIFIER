class Manager:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, a):
        self._size = a

obj = Manager(27)
print(obj.get_size())
obj.set_size(28)
print(obj.get_size())
