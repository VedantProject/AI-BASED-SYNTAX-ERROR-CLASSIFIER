class Processor:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, x):
        self._m = x

obj = Processor(33)
print(obj.get_m())
obj.set_m(45)
print(obj.get_m())
