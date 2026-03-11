class Manager:
    def __init__(self, b):
        self._b = b

    def get_b(self):
        return self._b

    def set_b(self, val):
        self._b = val

obj = Manager(12)
print(obj.get_b())
obj.set_b(23)
print(obj.get_b())
