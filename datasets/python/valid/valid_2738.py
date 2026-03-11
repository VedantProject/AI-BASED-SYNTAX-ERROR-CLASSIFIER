class Worker:
    def __init__(self, item):
        self._item = item

    def get_item(self):
        return self._item

    def set_item(self, temp):
        self._item = temp

obj = Worker(49)
print(obj.get_item())
obj.set_item(39)
print(obj.get_item())
