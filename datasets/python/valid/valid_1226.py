class Worker:
    def __init__(self, num):
        self._num = num

    def get_num(self):
        return self._num

    def set_num(self, m):
        self._num = m

obj = Worker(18)
print(obj.get_num())
obj.set_num(36)
print(obj.get_num())
