# flask-time-complexity-visualizer

A small Flask server that times an algorithm for growing input sizes, draws the
result as a chart, saves the chart as a PNG, and returns the data plus the
image (base64) as JSON.
 
## Setup
 
```
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
 
## Run
 
```
python app.py
```
 
The server runs on `http://localhost:8000`.
 
## Use it
 
```
http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10000
```
 
| Parameter | Meaning |
|-----------|---------|
| `algo`    | which algorithm to time (see the list below) |
| `step`    | gap between input sizes, e.g. `10` gives n = 0, 10, 20, ... |
| `n_max`   | biggest input size (`10000` and `10,000` both work) |
 
The smallest input size is always 0.
 
The JSON reply contains `input_sizes`, `times` (seconds), `image_path` (where the
PNG was saved, inside `plots/`) and `image_base64` (the same PNG as text).
 
## Algorithms
 
| `algo=`          | Complexity |
|------------------|------------|
| `linear_search`  | O(n) |
| `binary_search`  | O(log n) |
| `bubble_sort`    | O(n^2) |
| `selection_sort` | O(n^2) |
| `insertion_sort` | O(n^2) |
| `merge_sort`     | O(n log n) |
| `quick_sort`     | O(n log n) |
| `nested_loops`   | O(n^2) |
| `stack_balanced_parentheses`      | O(n) |
| `stack_reverse_string`            | O(n) |
| `stack_evaluate_postfix`          | O(n) |
| `queue_generate_binary_numbers`   | O(n) |
| `queue_bfs_traversal`             | O(n) |
 
Each one is timed on its worst case (item not found, or a reversed list).
Each size is timed 3 times and the fastest run is kept, so random slowdowns
don't spoil the chart.
The `stack_*` algorithms run on a custom `Stack` (`stack.py`) and the `queue_*`
algorithms run on a custom `Queue` (`queue_ds.py`) — both array/deque-based
with their own test suites.

 
Tip: the O(n^2) algorithms get slow with big inputs. Try
`algo=bubble_sort&step=100&n_max=2000`. A request stops by itself after 30 seconds.
 
## Tests
 
```
python -m unittest -v
```
 
## Files
 
| File | Purpose |
|------|---------|
| `app.py` | the visualizer function and the Flask endpoint |
| `algorithms.py` | the algorithms that get timed |
| `stack.py` | Stack data structure used by the `stack_*` algorithms |
| `queue_ds.py` | Queue data structure used by the `queue_*` algorithms |
| `test_app.py` | tests |
| `test_stack.py` | Stack tests |
| `test_queue_ds.py` | Queue tests |
| `requirements.txt` | packages to install |
| `plots/` | saved chart images |
