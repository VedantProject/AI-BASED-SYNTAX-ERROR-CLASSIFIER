class Manager:
    def __init__(self, b):
        self._b = b

    def get_b(self):
        return self._b

    def set_b(self, num):
        self._b = num

obj = Manager(38)
print(obj.get_b())
obj.set_b(11)
print(obj.get_b())
