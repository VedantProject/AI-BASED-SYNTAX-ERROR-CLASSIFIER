class Manager:
    def __init__(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_result(self, n):
        self._result = n

obj = Manager(37)
print(obj.get_result())
obj.set_result(12)
print(obj.get_result())
