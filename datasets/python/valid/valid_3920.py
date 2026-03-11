class Stack:
    def __init__(self):
        self._data = []

    def push(self, diff):
        self._data.append(diff)

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

s = Stack()
for i in [80, 23, 81, 59, 86]:
    s.push(i)
print(s.pop())
print(s.peek())
