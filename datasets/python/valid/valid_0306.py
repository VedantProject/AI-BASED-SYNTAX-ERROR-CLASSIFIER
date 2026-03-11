class Stack:
    def __init__(self):
        self._data = []

    def push(self, temp):
        self._data.append(temp)

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

s = Stack()
for i in [46, 10, 88, 74]:
    s.push(i)
print(s.pop())
print(s.peek())
