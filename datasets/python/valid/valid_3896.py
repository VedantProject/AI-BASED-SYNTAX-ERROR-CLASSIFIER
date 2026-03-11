class Handler:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, m):
        self._count = m

obj = Handler(14)
print(obj.get_count())
obj.set_count(30)
print(obj.get_count())
