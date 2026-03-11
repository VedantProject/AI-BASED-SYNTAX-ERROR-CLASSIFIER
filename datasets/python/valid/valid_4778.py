class Engine:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, n):
        self._count = n

obj = Engine(20)
print(obj.get_count())
obj.set_count(11)
print(obj.get_count())
