"""Queue (FIFO), backed by collections.deque.

Named queue_ds.py (not queue.py) so it doesn't shadow Python's
built-in `queue` module, which Flask/other libraries may import.
"""

from collections import deque


class QueueError(Exception):
    """Raised for illegal operations on an empty Queue."""


class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise QueueError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        if self.is_empty():
            raise QueueError("peek from empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __len__(self):
        return self.size()

    def __repr__(self):
        return f"Queue({list(self._items)})"