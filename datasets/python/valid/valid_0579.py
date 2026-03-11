class Processor:
    def __init__(self, result):
        self._result = result

    def get_result(self):
        return self._result

    def set_result(self, item):
        self._result = item

obj = Processor(46)
print(obj.get_result())
obj.set_result(7)
print(obj.get_result())
