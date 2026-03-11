class Manager:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, val):
        self._num = val

obj = Manager(36)
print(obj.get_num())
obj.set_num(19)
print(obj.get_num())
