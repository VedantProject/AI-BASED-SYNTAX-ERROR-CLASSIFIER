class Manager:
    def __init__(self, m):
        self._m = m

    def get_m(self):
        return self._m

    def set_m(self, num):
        self._m = num

obj = Manager(2)
print(obj.get_m())
obj.set_m(11)
print(obj.get_m())
