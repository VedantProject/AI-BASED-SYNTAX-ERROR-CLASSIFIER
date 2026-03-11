class Analyzer:
    _count = 0

    def __init__(self, b):
        self.value = b
        Analyzer._count += 1

    @staticmethod
    def get_count():
        return Analyzer._count

    def double(self):
        return self.value * 2

objs = [Analyzer(i) for i in range(7)]
print(f"Created: {Analyzer.get_count()} objects")
print([o.double() for o in objs])
