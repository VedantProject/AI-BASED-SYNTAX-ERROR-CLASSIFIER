class Calculator:
    def __init__(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_result(self, x):
        self._result = x

obj = Calculator(37)
print(obj.get_result())
obj.set_result(30)
print(obj.get_result())
