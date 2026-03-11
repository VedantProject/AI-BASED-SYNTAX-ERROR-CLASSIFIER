class Scanner:
    def __init__(self, z):
        self._z = z

    def get_z(self):
        return self._z

    def set_z(self, res):
        self._z = res

obj = Scanner(9)
print(obj.get_z())
obj.set_z(49)
print(obj.get_z())
