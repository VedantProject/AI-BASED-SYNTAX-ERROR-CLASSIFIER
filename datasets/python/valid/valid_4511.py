class Manager:
    def __init__(self, n):
        self._n = n

    def get_n(self):
        return self._n

    def set_n(self, m):
        self._n = m

obj = Manager(7)
print(obj.get_n())
obj.set_n(14)
print(obj.get_n())
