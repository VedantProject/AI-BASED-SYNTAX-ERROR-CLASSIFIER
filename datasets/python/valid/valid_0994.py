class Analyzer:
    def __init__(self, b):
        self._b = b

    def get_b(self):
        return self._b

    def set_b(self, diff):
        self._b = diff

obj = Analyzer(20)
print(obj.get_b())
obj.set_b(8)
print(obj.get_b())
