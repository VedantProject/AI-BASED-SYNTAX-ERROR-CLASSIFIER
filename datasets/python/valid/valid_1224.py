class Builder:
    def __init__(self, a):
        self._a = a

    def get_a(self):
        return self._a

    def set_a(self, b):
        self._a = b

obj = Builder(19)
print(obj.get_a())
obj.set_a(46)
print(obj.get_a())
