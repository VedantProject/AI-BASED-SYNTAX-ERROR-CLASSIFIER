class Handler:
    def __init__(self, n):
        self._n = n

    def get_n(self):
        return self._n

    def set_n(self, num):
        self._n = num

obj = Handler(45)
print(obj.get_n())
obj.set_n(8)
print(obj.get_n())
