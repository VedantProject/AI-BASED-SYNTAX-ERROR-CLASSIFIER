class Calculator:
    def __init__(self, item):
        self._item = item

    def get_item(self):
        return self._item

    def set_item(self, b):
        self._item = b

obj = Calculator(33)
print(obj.get_item())
obj.set_item(6)
print(obj.get_item())
