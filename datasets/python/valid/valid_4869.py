class Analyzer:
    def __init__(self, z):
        self._z = z

    def get_z(self):
        return self._z

    def set_z(self, result):
        self._z = result

obj = Analyzer(32)
print(obj.get_z())
obj.set_z(10)
print(obj.get_z())
