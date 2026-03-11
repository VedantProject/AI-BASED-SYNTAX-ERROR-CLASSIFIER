class Builder:
    def __init__(self, temp):
        self._temp = temp

    def get_temp(self):
        return self._temp

    def set_temp(self, num):
        self._temp = num

obj = Builder(34)
print(obj.get_temp())
obj.set_temp(33)
print(obj.get_temp())
