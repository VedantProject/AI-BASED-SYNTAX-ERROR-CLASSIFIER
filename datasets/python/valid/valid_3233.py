class Tracker:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, b):
        self._y = b

obj = Tracker(40)
print(obj.get_y())
obj.set_y(33)
print(obj.get_y())
