class Analyzer:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, temp):
        self._m = temp

obj = Analyzer(23)
print(obj.get_m())
obj.set_m(25)
print(obj.get_m())
