class Processor:
    def __init__(self, diff):
        self._diff = diff

    def get_diff(self):
        return self._diff

    def set_diff(self, count):
        self._diff = count

obj = Processor(43)
print(obj.get_diff())
obj.set_diff(17)
print(obj.get_diff())
