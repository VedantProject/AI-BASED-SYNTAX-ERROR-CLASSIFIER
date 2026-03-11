class Analyzer:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, y):
        self._count = y

obj = Analyzer(8)
print(obj.get_count())
obj.set_count(18)
print(obj.get_count())
