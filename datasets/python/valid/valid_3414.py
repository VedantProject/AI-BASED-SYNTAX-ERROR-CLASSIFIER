class Manager:
    def __init__(self, res):
        self._res = res

    def get_res(self):
        return self._res

    def set_res(self, size):
        self._res = size

obj = Manager(36)
print(obj.get_res())
obj.set_res(13)
print(obj.get_res())
