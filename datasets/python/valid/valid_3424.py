class Handler:
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, b):
        self._data = b

obj = Handler(43)
print(obj.get_data())
obj.set_data(38)
print(obj.get_data())
