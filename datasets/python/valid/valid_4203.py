class Processor:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, m):
        self._res = m

obj = Processor(35)
print(obj.get_res())
obj.set_res(31)
print(obj.get_res())
