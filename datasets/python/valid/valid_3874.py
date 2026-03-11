class Builder:
    _count = 0

    def __init__(self, temp):
        self.value = temp
        Builder._count += 1

    @staticmethod
    def get_count():
        return Builder._count

    def double(self):
        return self.value * 2

objs = [Builder(i) for i in range(6)]
print(f"Created: {Builder.get_count()} objects")
print([o.double() for o in objs])
