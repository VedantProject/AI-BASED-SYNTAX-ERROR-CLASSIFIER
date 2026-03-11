class Processor:
    def __init__(self, acc):
        self._acc = acc

    def get_acc(self):
        return self._acc

    def set_acc(self, prod):
        self._acc = prod

obj = Processor(26)
print(obj.get_acc())
obj.set_acc(45)
print(obj.get_acc())
