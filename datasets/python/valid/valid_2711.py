class Manager:
    def __init__(self, count):
        self._count = count

    def get_count(self):
        return self._count

    def set_count(self, result):
        self._count = result

obj = Manager(25)
print(obj.get_count())
obj.set_count(32)
print(obj.get_count())
