class Processor:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, size):
        self._num = size

obj = Processor(44)
print(obj.get_num())
obj.set_num(14)
print(obj.get_num())
