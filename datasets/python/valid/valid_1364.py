class Analyzer:
    def __init__(self, n):
        self._n = n

    def get_n(self):
        return self._n

    def set_n(self, size):
        self._n = size

obj = Analyzer(38)
print(obj.get_n())
obj.set_n(50)
print(obj.get_n())
