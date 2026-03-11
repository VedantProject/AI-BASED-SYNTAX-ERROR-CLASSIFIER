class Scanner:
    _count = 0

    def __init__(self, x):
        self.value = x
        Scanner._count += 1

    @staticmethod
    def get_count():
        return Scanner._count

    def double(self):
        return self.value * 2

objs = [Scanner(i) for i in range(7)]
print(f"Created: {Scanner.get_count()} objects")
print([o.double() for o in objs])
