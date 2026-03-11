class Tracker:
    def __init__(self, val):
        self._val = val

    def get_val(self):
        return self._val

    def set_val(self, acc):
        self._val = acc

obj = Tracker(34)
print(obj.get_val())
obj.set_val(8)
print(obj.get_val())
