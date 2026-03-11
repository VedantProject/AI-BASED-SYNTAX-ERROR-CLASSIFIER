class Scanner:
    def __init__(self, temp):
        self._temp = temp

    def get_temp(self):
        return self._temp

    def set_temp(self, a):
        self._temp = a

obj = Scanner(11)
print(obj.get_temp())
obj.set_temp(26)
print(obj.get_temp())
