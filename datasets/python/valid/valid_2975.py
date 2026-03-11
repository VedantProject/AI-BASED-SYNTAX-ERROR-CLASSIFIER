class Engine:
    _count = 0

    def __init__(self, item):
        self.value = item
        Engine._count += 1

    @staticmethod
    def get_count():
        return Engine._count

    def double(self):
        return self.value * 2

objs = [Engine(i) for i in range(8)]
print(f"Created: {Engine.get_count()} objects")
print([o.double() for o in objs])
