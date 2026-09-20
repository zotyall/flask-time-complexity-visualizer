# The algorithms we time. Each one takes n (the input size), builds its own
# worst-case input, and runs. The visualizer in app.py just calls algorithm(n).


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


def nested_loops(n):               # O(n^2)
    for i in range(n):
        for j in range(n):
            pass


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
}
