class Manager:
    def __init__(self, temp):
        self._temp = temp

    def get_temp(self):
        return self._temp

    def set_temp(self, res):
        self._temp = res

obj = Manager(29)
print(obj.get_temp())
obj.set_temp(9)
print(obj.get_temp())
