class Handler:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, item):
        self._res = item

obj = Handler(16)
print(obj.get_res())
obj.set_res(25)
print(obj.get_res())
