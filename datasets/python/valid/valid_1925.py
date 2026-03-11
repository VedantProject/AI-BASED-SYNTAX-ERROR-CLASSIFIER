class Engine:
    def __init__(self, b):
        self._b = b

    def get_b(self):
        return self._b

    def set_b(self, n):
        self._b = n

obj = Engine(38)
print(obj.get_b())
obj.set_b(24)
print(obj.get_b())
