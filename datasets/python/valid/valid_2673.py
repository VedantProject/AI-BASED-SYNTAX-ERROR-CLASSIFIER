class Analyzer:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, prod):
        self._m = prod

obj = Analyzer(32)
print(obj.get_m())
obj.set_m(38)
print(obj.get_m())
