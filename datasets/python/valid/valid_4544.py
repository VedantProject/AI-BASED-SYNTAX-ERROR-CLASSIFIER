class Worker:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, a):
        self._count = a

obj = Worker(16)
print(obj.get_count())
obj.set_count(18)
print(obj.get_count())
