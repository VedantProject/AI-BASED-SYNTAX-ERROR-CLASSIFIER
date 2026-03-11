class Scanner:
    def __init__(self, prod):
        self._prod = prod

    def get_prod(self):
        return self._prod

    def set_prod(self, num):
        self._prod = num

obj = Scanner(40)
print(obj.get_prod())
obj.set_prod(9)
print(obj.get_prod())
