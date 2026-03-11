class Tracker:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, res):
        self._num = res

obj = Tracker(9)
print(obj.get_num())
obj.set_num(37)
print(obj.get_num())
