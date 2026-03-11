class Processor:
    def __init__(self, z):
        self._z = z

    def get_z(self):
        return self._z

    def set_z(self, m):
        self._z = m

obj = Processor(48)
print(obj.get_z())
obj.set_z(44)
print(obj.get_z())
