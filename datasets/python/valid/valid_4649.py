class Engine:
    def __init__(self, val):
        self._val = val

    def get_val(self):
        return self._val

    def set_val(self, data):
        self._val = data

obj = Engine(3)
print(obj.get_val())
obj.set_val(2)
print(obj.get_val())
