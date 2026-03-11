class Worker:
    def __init__(self, n):
        self._n = n

    def get_n(self):
        return self._n

    def set_n(self, y):
        self._n = y

obj = Worker(27)
print(obj.get_n())
obj.set_n(43)
print(obj.get_n())
