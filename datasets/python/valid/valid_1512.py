class Worker:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, prod):
        self._res = prod

obj = Worker(10)
print(obj.get_res())
obj.set_res(19)
print(obj.get_res())
