class Scanner:
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def set_data(self, total):
        self._data = total

obj = Scanner(40)
print(obj.get_data())
obj.set_data(7)
print(obj.get_data())
