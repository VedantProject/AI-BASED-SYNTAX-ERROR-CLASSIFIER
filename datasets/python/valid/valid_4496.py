class Calculator:
    _count = 0

    def __init__(self, diff):
        self.value = diff
        Calculator._count += 1

    @staticmethod
    def get_count():
        return Calculator._count

    def double(self):
        return self.value * 2

objs = [Calculator(i) for i in range(6)]
print(f"Created: {Calculator.get_count()} objects")
print([o.double() for o in objs])
