import unittest

from queue_ds import Queue, QueueError


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_new_queue_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.assertEqual(self.queue.size(), 0)
        self.assertEqual(len(self.queue), 0)

    def test_enqueue_increases_size(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.size(), 2)
        self.assertFalse(self.queue.is_empty())

    def test_peek_returns_first_enqueued_without_removing(self):
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.peek(), 1)
        self.assertEqual(self.queue.size(), 2)

    def test_dequeue_returns_in_fifo_order(self):
        for i in range(5):
            self.queue.enqueue(i)
        dequeued = [self.queue.dequeue() for _ in range(5)]
        self.assertEqual(dequeued, [0, 1, 2, 3, 4])
        self.assertTrue(self.queue.is_empty())

    def test_dequeue_empty_raises(self):
        with self.assertRaises(QueueError):
            self.queue.dequeue()

    def test_peek_empty_raises(self):
        with self.assertRaises(QueueError):
            self.queue.peek()

    def test_mixed_enqueue_dequeue_sequence(self):
        self.queue.enqueue("a")
        self.queue.enqueue("b")
        self.assertEqual(self.queue.dequeue(), "a")
        self.queue.enqueue("c")
        self.assertEqual(self.queue.dequeue(), "b")
        self.assertEqual(self.queue.dequeue(), "c")
        self.assertTrue(self.queue.is_empty())

    def test_repr_does_not_error(self):
        self.queue.enqueue(1)
        self.assertIn("Queue", repr(self.queue))


if __name__ == "__main__":
    unittest.main()