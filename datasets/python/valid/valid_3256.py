class Analyzer:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, prod):
        self._num = prod

obj = Analyzer(30)
print(obj.get_num())
obj.set_num(18)
print(obj.get_num())
