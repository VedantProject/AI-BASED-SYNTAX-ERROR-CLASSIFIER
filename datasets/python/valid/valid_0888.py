class Scanner:
    def __init__(self, z):
        self._z = z

    def get_z(self):
        return self._z

    def set_z(self, temp):
        self._z = temp

obj = Scanner(47)
print(obj.get_z())
obj.set_z(27)
print(obj.get_z())
