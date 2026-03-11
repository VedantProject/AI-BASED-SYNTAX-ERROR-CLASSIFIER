class Processor:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, prod):
        self._count = prod

obj = Processor(43)
print(obj.get_count())
obj.set_count(13)
print(obj.get_count())
