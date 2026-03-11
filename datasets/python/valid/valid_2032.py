class Manager:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, prod):
        self._y = prod

obj = Manager(39)
print(obj.get_y())
obj.set_y(44)
print(obj.get_y())
