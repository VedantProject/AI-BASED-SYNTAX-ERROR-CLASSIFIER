class Processor:
    def __init__(self, prod):
        self._prod = prod

    def get_prod(self):
        return self._prod

    def set_prod(self, item):
        self._prod = item

obj = Processor(24)
print(obj.get_prod())
obj.set_prod(21)
print(obj.get_prod())
