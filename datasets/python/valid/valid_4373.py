class Processor:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, m):
        self._count = m

obj = Processor(21)
print(obj.get_count())
obj.set_count(25)
print(obj.get_count())
