class Calculator:
    _count = 0

    def __init__(self, n):
        self.value = n
        Calculator._count += 1

    @staticmethod
    def get_count():
        return Calculator._count

    def double(self):
        return self.value * 2

objs = [Calculator(i) for i in range(10)]
print(f"Created: {Calculator.get_count()} objects")
print([o.double() for o in objs])
