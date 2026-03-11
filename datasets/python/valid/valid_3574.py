class Manager:
    def __init__(self, acc):
        self._acc = acc

    def get_acc(self):
        return self._acc

    def set_acc(self, temp):
        self._acc = temp

obj = Manager(8)
print(obj.get_acc())
obj.set_acc(4)
print(obj.get_acc())
