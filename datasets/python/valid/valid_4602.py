class Analyzer:
    def __init__(self, prod):
        self._prod = prod

    def get_prod(self):
        return self._prod

    def set_prod(self, y):
        self._prod = y

obj = Analyzer(40)
print(obj.get_prod())
obj.set_prod(10)
print(obj.get_prod())
