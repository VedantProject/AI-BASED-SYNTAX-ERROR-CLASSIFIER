class Builder:
    def __init__(self, prod):
        self._prod = prod

    def get_prod(self):
        return self._prod

    def set_prod(self, total):
        self._prod = total

obj = Builder(15)
print(obj.get_prod())
obj.set_prod(13)
print(obj.get_prod())
