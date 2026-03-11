class Worker:
    def __init__(self, acc):
        self._acc = acc

    def get_acc(self):
        return self._acc

    def set_acc(self, total):
        self._acc = total

obj = Worker(41)
print(obj.get_acc())
obj.set_acc(28)
print(obj.get_acc())
