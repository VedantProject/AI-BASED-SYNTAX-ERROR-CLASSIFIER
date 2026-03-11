class Scanner:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, count):
        self._y = count

obj = Scanner(42)
print(obj.get_y())
obj.set_y(40)
print(obj.get_y())
