class Analyzer:
    def __init__(self, b):
        self._b = b

    def get_b(self):
        return self._b

    def set_b(self, acc):
        self._b = acc

obj = Analyzer(38)
print(obj.get_b())
obj.set_b(19)
print(obj.get_b())
