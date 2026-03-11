class Handler:
    _count = 0

    def __init__(self, b):
        self.value = b
        Handler._count += 1

    @staticmethod
    def get_count():
        return Handler._count

    def double(self):
        return self.value * 2

objs = [Handler(i) for i in range(8)]
print(f"Created: {Handler.get_count()} objects")
print([o.double() for o in objs])
