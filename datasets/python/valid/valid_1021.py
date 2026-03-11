class Scanner:
    _count = 0

    def __init__(self, acc):
        self.value = acc
        Scanner._count += 1

    @staticmethod
    def get_count():
        return Scanner._count

    def double(self):
        return self.value * 2

objs = [Scanner(i) for i in range(3)]
print(f"Created: {Scanner.get_count()} objects")
print([o.double() for o in objs])
