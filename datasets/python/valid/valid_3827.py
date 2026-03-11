class Tracker:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, data):
        self._y = data

obj = Tracker(28)
print(obj.get_y())
obj.set_y(27)
print(obj.get_y())
