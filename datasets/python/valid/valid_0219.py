class Builder:
    def __init__(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_result(self, acc):
        self._result = acc

obj = Builder(32)
print(obj.get_result())
obj.set_result(4)
print(obj.get_result())
