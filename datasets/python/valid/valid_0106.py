class Processor:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, x):
        self._res = x

obj = Processor(33)
print(obj.get_res())
obj.set_res(25)
print(obj.get_res())
