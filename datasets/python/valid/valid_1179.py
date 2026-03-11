class Handler:
    def __init__(self, prod):
        self._prod = prod

    def get_prod(self):
        return self._prod

    def set_prod(self, y):
        self._prod = y

obj = Handler(43)
print(obj.get_prod())
obj.set_prod(24)
print(obj.get_prod())
