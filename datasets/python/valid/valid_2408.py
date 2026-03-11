class Processor:
    def __init__(self, item):
        self._item = item

    def get_item(self):
        return self._item

    def set_item(self, x):
        self._item = x

obj = Processor(2)
print(obj.get_item())
obj.set_item(16)
print(obj.get_item())
