class Tracker:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, size):
        self._res = size

obj = Tracker(47)
print(obj.get_res())
obj.set_res(24)
print(obj.get_res())
