class Tracker:
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, result):
        self._data = result

obj = Tracker(24)
print(obj.get_data())
obj.set_data(47)
print(obj.get_data())
