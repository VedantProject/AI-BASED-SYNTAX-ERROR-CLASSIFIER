class Engine:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, prod):
        self._num = prod

obj = Engine(16)
print(obj.get_num())
obj.set_num(41)
print(obj.get_num())
