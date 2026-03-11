class Handler:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, size):
        self._y = size

obj = Handler(42)
print(obj.get_y())
obj.set_y(38)
print(obj.get_y())
