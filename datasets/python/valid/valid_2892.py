class Engine:
    _count = 0

    def __init__(self, temp):
        self.value = temp
        Engine._count += 1

    @staticmethod
    def get_count():
        return Engine._count

    def double(self):
        return self.value * 2

objs = [Engine(i) for i in range(4)]
print(f"Created: {Engine.get_count()} objects")
print([o.double() for o in objs])
