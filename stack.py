"""Array-based Stack (LIFO)."""


class StackError(Exception):
    """Raised for illegal operations on an empty Stack."""


class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise StackError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise StackError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __len__(self):
        return self.size()

    def __repr__(self):
        return f"Stack({self._items})"