# The algorithms we time. Each one takes n (the input size), builds its own
# worst-case input, and runs. The visualizer in app.py just calls algorithm(n).
import random

from stack import Stack
from queue_ds import Queue


def linear_search(n):              # O(n)
    for v in range(n):             # range(n) acts like the list [0..n-1] but costs nothing to create
        if v == -1:                # -1 is never in it, so every item gets checked (worst case)
            return True
    return False


def binary_search(n):              # O(log n)
    a, x = range(n), -1            # sorted "list", and a value that is not in it (worst case)
    for _ in range(1000):          # one search is too fast to time, so repeat it 1000 times
        lo, hi = 0, n - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if a[mid] == x:
                break
            elif a[mid] < x:
                lo = mid + 1
            else:
                hi = mid - 1


def bubble_sort(n):                # O(n^2)
    a = list(range(n, 0, -1))      # reversed list = worst case
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


def selection_sort(n):             # O(n^2)
    a = list(range(n, 0, -1))
    for i in range(n):
        m = i                      # position of the smallest item so far
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]
    return a


def insertion_sort(n):             # O(n^2)
    a = list(range(n, 0, -1))
    for i in range(1, n):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(n):                 # O(n log n)
    return _merge_sort(list(range(n, 0, -1)))


def _merge_sort(a):                # split in half, sort each half, then merge the halves
    if len(a) <= 1:
        return a
    left, right = _merge_sort(a[:len(a) // 2]), _merge_sort(a[len(a) // 2:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    return out + left[i:] + right[j:]


def quick_sort(n):                 # O(n log n)
    return _quick_sort(list(range(n, 0, -1)))


def _quick_sort(a):                # middle item is the pivot: smaller go left, bigger go right
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    return (_quick_sort([x for x in a if x < pivot]) + [x for x in a if x == pivot]
            + _quick_sort([x for x in a if x > pivot]))


def nested_loops(n):

    unique_users =[]               # O(n^2)
    for i in range(n):
        seen = False
        for j in range(n):
            if nested_loops[i]['id'] == unique_users[j]['id']:
                seen = True
                break
        if not seen:
            unique_users.append(nested_loops[i])


# --- Stack-based algorithms ---

_PAIRS = {")": "(", "]": "[", "}": "{"}
_OPENERS = set(_PAIRS.values())


def _make_balanced_string(n):      # a balanced-parentheses string with n opens + n closes
    if n == 0:
        return ""
    result, open_count, close_count = [], 0, 0
    while open_count < n or close_count < n:
        can_open = open_count < n
        can_close = close_count < open_count
        if can_open and (not can_close or random.random() < 0.5):
            result.append("(")
            open_count += 1
        else:
            result.append(")")
            close_count += 1
    return "".join(result)


def stack_balanced_parentheses(n):  # O(n) — push openers, pop on matching closer
    expression = _make_balanced_string(n)
    stack = Stack()
    for ch in expression:
        if ch in _OPENERS:
            stack.push(ch)
        elif ch in _PAIRS:
            if stack.is_empty() or stack.pop() != _PAIRS[ch]:
                return False
    return stack.is_empty()


def stack_reverse_string(n):        # O(n) — push every char then pop to build the reverse
    s = "".join(chr(97 + (i % 26)) for i in range(n))
    stack = Stack()
    for ch in s:
        stack.push(ch)
    reversed_chars = []
    while not stack.is_empty():
        reversed_chars.append(stack.pop())
    return "".join(reversed_chars)


def _make_postfix_expression(n):    # a valid postfix expression with n operands
    if n == 0:
        return []
    operators = ["+", "-", "*"]
    tokens, operand_count = ["1"], 1
    while operand_count < n:
        tokens.append(str(random.randint(1, 9)))
        operand_count += 1
        tokens.append(random.choice(operators))
    return tokens


def stack_evaluate_postfix(n):      # O(n) — evaluate a postfix expression with n operands
    tokens = _make_postfix_expression(n)
    stack = Stack()
    for token in tokens:
        if token in ("+", "-", "*"):
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.push(a + b)
            elif token == "-":
                stack.push(a - b)
            else:
                stack.push(a * b)
        else:
            stack.push(int(token))
    return stack.pop() if not stack.is_empty() else None


# --- Queue-based algorithms ---

def queue_generate_binary_numbers(n):  # O(n) — BFS over a bit-tree with a Queue
    if n <= 0:
        return []
    result = []
    q = Queue()
    q.enqueue("1")
    for _ in range(n):
        front = q.dequeue()
        result.append(front)
        q.enqueue(front + "0")
        q.enqueue(front + "1")
    return result


def _make_graph(n):                 # a connected graph: random tree + a few extra edges
    graph = {i: [] for i in range(n)}
    for i in range(1, n):
        parent = random.randint(0, i - 1)
        graph[parent].append(i)
        graph[i].append(parent)
    for _ in range(min(n // 4, 20)):
        a, b = random.randint(0, n - 1), random.randint(0, n - 1)
        if a != b:
            graph[a].append(b)
            graph[b].append(a)
    return graph


def queue_bfs_traversal(n):         # O(n + e) — breadth-first traversal with a Queue
    if n <= 0:
        return []
    graph = _make_graph(n)
    visited = {0}
    order = []
    q = Queue()
    q.enqueue(0)
    while not q.is_empty():
        node = q.dequeue()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.enqueue(neighbor)
    return order


# name used in the URL -> function
ALGOS = {
    'linear_search': linear_search,
    'binary_search': binary_search,
    'bubble_sort': bubble_sort,
    'selection_sort': selection_sort,
    'insertion_sort': insertion_sort,
    'merge_sort': merge_sort,
    'quick_sort': quick_sort,
    'nested_loops': nested_loops,
    'stack_balanced_parentheses': stack_balanced_parentheses,
    'stack_reverse_string': stack_reverse_string,
    'stack_evaluate_postfix': stack_evaluate_postfix,
    'queue_generate_binary_numbers': queue_generate_binary_numbers,
    'queue_bfs_traversal': queue_bfs_traversal,
}