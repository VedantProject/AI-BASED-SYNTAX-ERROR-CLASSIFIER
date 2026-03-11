class Tracker:
    _count = 0

    def __init__(self, y):
        self.value = y
        Tracker._count += 1

    @staticmethod
    def get_count():
        return Tracker._count

    def double(self):
        return self.value * 2

objs = [Tracker(i) for i in range(2)]
print(f"Created: {Tracker.get_count()} objects")
print([o.double() for o in objs])
