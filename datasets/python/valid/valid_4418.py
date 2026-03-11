class Builder:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, res):
        self._y = res

obj = Builder(34)
print(obj.get_y())
obj.set_y(21)
print(obj.get_y())
