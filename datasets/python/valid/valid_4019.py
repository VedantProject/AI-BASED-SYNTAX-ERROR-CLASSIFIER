class Scanner:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, num):
        self._count = num

obj = Scanner(27)
print(obj.get_count())
obj.set_count(36)
print(obj.get_count())
