class Tracker:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, n):
        self._res = n

obj = Tracker(30)
print(obj.get_res())
obj.set_res(17)
print(obj.get_res())
