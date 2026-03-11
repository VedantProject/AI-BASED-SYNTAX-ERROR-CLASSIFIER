class Scanner:
    def __init__(self, acc):
        self._acc = acc

    def get_acc(self):
        return self._acc

    def set_acc(self, n):
        self._acc = n

obj = Scanner(48)
print(obj.get_acc())
obj.set_acc(50)
print(obj.get_acc())
