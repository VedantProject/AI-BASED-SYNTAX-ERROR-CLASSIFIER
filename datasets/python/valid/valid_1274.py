class Analyzer:
    def __init__(self, a):
        self._a = a

    def get_a(self):
        return self._a

    def set_a(self, result):
        self._a = result

obj = Analyzer(14)
print(obj.get_a())
obj.set_a(39)
print(obj.get_a())
