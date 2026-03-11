class Handler:
    def __init__(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_result(self, item):
        self._result = item

obj = Handler(36)
print(obj.get_result())
obj.set_result(4)
print(obj.get_result())
