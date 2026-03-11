class Manager:
    _count = 0

    def __init__(self, res):
        self.value = res
        Manager._count += 1

    @staticmethod
    def get_count():
        return Manager._count

    def double(self):
        return self.value * 2

objs = [Manager(i) for i in range(8)]
print(f"Created: {Manager.get_count()} objects")
print([o.double() for o in objs])
