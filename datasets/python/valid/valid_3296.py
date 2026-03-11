class Scanner:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, z):
        self._count = z

obj = Scanner(32)
print(obj.get_count())
obj.set_count(38)
print(obj.get_count())
