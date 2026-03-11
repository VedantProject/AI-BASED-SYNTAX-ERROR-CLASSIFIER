class Engine:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, total):
        self._size = total

obj = Engine(3)
print(obj.get_size())
obj.set_size(23)
print(obj.get_size())
