class Worker:
    def __init__(self, val):
        self._val = val

    def get_val(self):
        return self._val

    def set_val(self, diff):
        self._val = diff

obj = Worker(10)
print(obj.get_val())
obj.set_val(8)
print(obj.get_val())
