class Processor:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, temp):
        self._res = temp

obj = Processor(41)
print(obj.get_res())
obj.set_res(40)
print(obj.get_res())
