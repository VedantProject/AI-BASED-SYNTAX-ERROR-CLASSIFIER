class Manager:
    _count = 0

    def __init__(self, diff):
        self.value = diff
        Manager._count += 1

    @staticmethod
    def get_count():
        return Manager._count

    def double(self):
        return self.value * 2

objs = [Manager(i) for i in range(5)]
print(f"Created: {Manager.get_count()} objects")
print([o.double() for o in objs])
