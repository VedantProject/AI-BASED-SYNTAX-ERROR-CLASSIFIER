class Engine:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, prod):
        self._m = prod

obj = Engine(50)
print(obj.get_m())
obj.set_m(40)
print(obj.get_m())
