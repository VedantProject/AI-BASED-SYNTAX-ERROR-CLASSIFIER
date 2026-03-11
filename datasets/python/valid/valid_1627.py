class Tracker:
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, item):
        self._data = item

obj = Tracker(34)
print(obj.get_data())
obj.set_data(9)
print(obj.get_data())
