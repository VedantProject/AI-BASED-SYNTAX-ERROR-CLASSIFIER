class Worker:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, temp):
        self._size = temp

obj = Worker(49)
print(obj.get_size())
obj.set_size(30)
print(obj.get_size())
