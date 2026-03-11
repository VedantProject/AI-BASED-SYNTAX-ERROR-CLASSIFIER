class Engine:
    def __init__(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_result(self, data):
        self._result = data

obj = Engine(15)
print(obj.get_result())
obj.set_result(38)
print(obj.get_result())
