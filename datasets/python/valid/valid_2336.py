class Builder:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, size):
        self._num = size

obj = Builder(19)
print(obj.get_num())
obj.set_num(5)
print(obj.get_num())
