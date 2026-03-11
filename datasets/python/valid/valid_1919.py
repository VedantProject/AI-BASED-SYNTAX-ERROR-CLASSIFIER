class Analyzer:
    def __init__(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_result(self, a):
        self._result = a

obj = Analyzer(42)
print(obj.get_result())
obj.set_result(41)
print(obj.get_result())
