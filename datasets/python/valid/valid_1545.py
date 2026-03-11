class Scanner:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, result):
        self._m = result

obj = Scanner(16)
print(obj.get_m())
obj.set_m(21)
print(obj.get_m())
