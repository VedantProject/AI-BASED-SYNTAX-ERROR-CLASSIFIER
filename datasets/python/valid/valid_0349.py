class Analyzer:
    def __init__(self, temp):
        self._temp = temp

    def get_temp(self):
        return self._temp

    def set_temp(self, acc):
        self._temp = acc

obj = Analyzer(35)
print(obj.get_temp())
obj.set_temp(35)
print(obj.get_temp())
