class Worker:
    def __init__(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def set_y(self, m):
        self._y = m

obj = Worker(8)
print(obj.get_y())
obj.set_y(28)
print(obj.get_y())
