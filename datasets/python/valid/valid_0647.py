class Tracker:
    def __init__(self, diff):
        self._diff = diff

    def get_diff(self):
        return self._diff

    def set_diff(self, data):
        self._diff = data

obj = Tracker(16)
print(obj.get_diff())
obj.set_diff(20)
print(obj.get_diff())
