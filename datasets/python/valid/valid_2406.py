class Tracker:
    def __init__(self, temp):
        self._temp = temp

    def get_temp(self):
        return self._temp

    def set_temp(self, prod):
        self._temp = prod

obj = Tracker(15)
print(obj.get_temp())
obj.set_temp(47)
print(obj.get_temp())
