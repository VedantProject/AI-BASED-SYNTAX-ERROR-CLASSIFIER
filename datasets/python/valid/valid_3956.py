class Stack:
    def __init__(self):
        self._data = []

    def push(self, acc):
        self._data.append(acc)

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

s = Stack()
for i in [53, 18, 97, 25, 95]:
    s.push(i)
print(s.pop())
print(s.peek())
