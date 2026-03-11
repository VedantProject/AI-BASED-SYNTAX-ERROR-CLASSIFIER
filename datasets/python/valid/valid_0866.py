class Scanner:
    def __init__(self, a):
        self._a = a

    def get_a(self):
        return self._a

    def set_a(self, m):
        self._a = m

obj = Scanner(24)
print(obj.get_a())
obj.set_a(16)
print(obj.get_a())
