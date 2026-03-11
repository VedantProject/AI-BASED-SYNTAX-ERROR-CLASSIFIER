class Worker:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, n):
        self._x = n

obj = Worker(4)
print(obj.get_x())
obj.set_x(19)
print(obj.get_x())
