class Engine:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, z):
        self._num = z

obj = Engine(26)
print(obj.get_num())
obj.set_num(30)
print(obj.get_num())
