import unittest

from stack import Stack, StackError


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_new_stack_is_empty(self):
        self.assertTrue(self.stack.is_empty())
        self.assertEqual(self.stack.size(), 0)
        self.assertEqual(len(self.stack), 0)

    def test_push_increases_size(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.size(), 2)
        self.assertFalse(self.stack.is_empty())

    def test_peek_returns_last_pushed_without_removing(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.peek(), 2)
        self.assertEqual(self.stack.size(), 2)

    def test_pop_returns_in_lifo_order(self):
        for i in range(5):
            self.stack.push(i)
        popped = [self.stack.pop() for _ in range(5)]
        self.assertEqual(popped, [4, 3, 2, 1, 0])
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty_raises(self):
        with self.assertRaises(StackError):
            self.stack.pop()

    def test_peek_empty_raises(self):
        with self.assertRaises(StackError):
            self.stack.peek()

    def test_mixed_push_pop_sequence(self):
        self.stack.push("a")
        self.stack.push("b")
        self.assertEqual(self.stack.pop(), "b")
        self.stack.push("c")
        self.assertEqual(self.stack.pop(), "c")
        self.assertEqual(self.stack.pop(), "a")
        self.assertTrue(self.stack.is_empty())

    def test_repr_does_not_error(self):
        self.stack.push(1)
        self.assertIn("Stack", repr(self.stack))


if __name__ == "__main__":
    unittest.main()