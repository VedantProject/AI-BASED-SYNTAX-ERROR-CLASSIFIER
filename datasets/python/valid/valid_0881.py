class Calculator:
    def __init__(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_result(self, n):
        self._result = n

obj = Calculator(15)
print(obj.get_result())
obj.set_result(9)
print(obj.get_result())
