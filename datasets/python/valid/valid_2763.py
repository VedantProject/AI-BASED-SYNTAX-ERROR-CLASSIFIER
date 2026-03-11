class Handler:
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, total):
        self._data = total

obj = Handler(31)
print(obj.get_data())
obj.set_data(16)
print(obj.get_data())
