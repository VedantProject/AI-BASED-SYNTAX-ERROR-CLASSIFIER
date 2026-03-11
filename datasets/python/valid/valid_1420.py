class Manager:
    def __init__(self, temp):
        self._temp = temp

    def get_temp(self):
        return self._temp

    def set_temp(self, data):
        self._temp = data

obj = Manager(10)
print(obj.get_temp())
obj.set_temp(32)
print(obj.get_temp())
