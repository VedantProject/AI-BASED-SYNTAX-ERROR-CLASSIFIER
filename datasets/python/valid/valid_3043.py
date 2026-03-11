class Processor:
    def __init__(self, diff):
        self._diff = diff

    def get_diff(self):
        return self._diff

    def set_diff(self, item):
        self._diff = item

obj = Processor(46)
print(obj.get_diff())
obj.set_diff(26)
print(obj.get_diff())
