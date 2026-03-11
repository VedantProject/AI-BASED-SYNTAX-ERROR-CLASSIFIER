class Worker:
    def __init__(self, a):
        self._a = a

    def get_a(self):
        return self._a

    def set_a(self, num):
        self._a = num

obj = Worker(4)
print(obj.get_a())
obj.set_a(20)
print(obj.get_a())
