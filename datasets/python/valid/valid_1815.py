class Processor:
    _count = 0

    def __init__(self, y):
        self.value = y
        Processor._count += 1

    @staticmethod
    def get_count():
        return Processor._count

    def double(self):
        return self.value * 2

objs = [Processor(i) for i in range(8)]
print(f"Created: {Processor.get_count()} objects")
print([o.double() for o in objs])
