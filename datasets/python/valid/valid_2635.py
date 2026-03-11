class Manager:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, temp):
        self._m = temp

obj = Manager(5)
print(obj.get_m())
obj.set_m(24)
print(obj.get_m())
