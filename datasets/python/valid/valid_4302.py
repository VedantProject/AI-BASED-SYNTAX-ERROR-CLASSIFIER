class Tracker:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, y):
        self._num = y

obj = Tracker(30)
print(obj.get_num())
obj.set_num(9)
print(obj.get_num())
