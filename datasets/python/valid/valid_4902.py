class Worker:
    def __init__(self, z):
        self._z = z

    def get_z(self):
        return self._z

    def set_z(self, item):
        self._z = item

obj = Worker(24)
print(obj.get_z())
obj.set_z(24)
print(obj.get_z())
