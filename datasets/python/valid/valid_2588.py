class Manager:
    def __init__(self, prod):
        self._prod = prod

    def get_prod(self):
        return self._prod

    def set_prod(self, b):
        self._prod = b

obj = Manager(36)
print(obj.get_prod())
obj.set_prod(34)
print(obj.get_prod())
