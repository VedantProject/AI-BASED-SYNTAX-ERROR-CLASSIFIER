class Analyzer:
    def __init__(self, z):
        self._z = z

    def get_z(self):
        return self._z

    def set_z(self, size):
        self._z = size

obj = Analyzer(29)
print(obj.get_z())
obj.set_z(12)
print(obj.get_z())
