class Worker:
    _count = 0

    def __init__(self, total):
        self.value = total
        Worker._count += 1

    @staticmethod
    def get_count():
        return Worker._count

    def double(self):
        return self.value * 2

objs = [Worker(i) for i in range(6)]
print(f"Created: {Worker.get_count()} objects")
print([o.double() for o in objs])
