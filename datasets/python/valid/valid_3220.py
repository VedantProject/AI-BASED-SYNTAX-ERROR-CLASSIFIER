class Manager:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, total):
        self._m = total

obj = Manager(46)
print(obj.get_m())
obj.set_m(27)
print(obj.get_m())
