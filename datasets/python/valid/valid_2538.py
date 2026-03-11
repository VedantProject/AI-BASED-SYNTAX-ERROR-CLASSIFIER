class Manager:
    def __init__(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_size(self, res):
        self._size = res

obj = Manager(25)
print(obj.get_size())
obj.set_size(45)
print(obj.get_size())
