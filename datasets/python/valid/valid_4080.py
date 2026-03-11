class Tracker:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, item):
        self._res = item

obj = Tracker(47)
print(obj.get_res())
obj.set_res(22)
print(obj.get_res())
