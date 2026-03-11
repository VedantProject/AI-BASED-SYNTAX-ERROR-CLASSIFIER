class Builder:
    def __init__(self, n):
        self._n = n

    def get_n(self):
        return self._n

    def set_n(self, res):
        self._n = res

obj = Builder(47)
print(obj.get_n())
obj.set_n(27)
print(obj.get_n())
