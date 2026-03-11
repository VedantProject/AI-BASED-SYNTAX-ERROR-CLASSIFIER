class Tracker:
    def __init__(self, item):
        self._item = item

    def get_item(self):
        return self._item

    def set_item(self, total):
        self._item = total

obj = Tracker(12)
print(obj.get_item())
obj.set_item(23)
print(obj.get_item())
