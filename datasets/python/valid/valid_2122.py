class Worker:
    def __init__(self, item):
        self._item = item

    def get_item(self):
        return self._item

    def set_item(self, num):
        self._item = num

obj = Worker(20)
print(obj.get_item())
obj.set_item(25)
print(obj.get_item())
