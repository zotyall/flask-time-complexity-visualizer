# Time complexity visualizer - Flask API
# Run:  python app.py
# Try:  http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10000
import base64
import os
import time
import matplotlib
matplotlib.use('Agg')  # was 'TkAgg': a server has no window to show
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request

from algorithms import ALGOS

app = Flask(__name__)
PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'plots')  # saved images go here


def time_complexity_visualizer(algorithm, n_min, n_max, n_step):
    times = []
    input_sizes = list(range(n_min, n_max + 1, n_step))   # was n_max + n_step (could pass n_max)
    begin = time.perf_counter()

    for n in input_sizes:
        if time.perf_counter() - begin > 30:               # too slow, stop here
            break
        runs = []
        for _ in range(3):                                 # run 3 times and keep the fastest (ignores random slowdowns)
            start_time = time.perf_counter()               # was time.time() (too coarse on Windows)
            algorithm(n)
            end_time = time.perf_counter()
            runs.append(end_time - start_time)
        times.append(min(runs))

    input_sizes = input_sizes[:len(times)]                 # same length as times if we stopped early
    fig, ax = plt.subplots()                               # was plt.subplots('Input size') -> crash
    ax.set_xlabel('Input size')
    ax.set_ylabel('Running time (seconds)')
    ax.set_title('Algorithm time complexity visualization')
    ax.plot(input_sizes, times, 'o-')
    return input_sizes, times, fig


@app.route('/')
def index():
    return jsonify(usage='/analyze?algo=linear_search&step=10&n_max=10000', algorithms=list(ALGOS))


@app.route('/analyze')
def analyze():
    algo = request.args.get('algo', '').strip("[]'\" ")                # ?algo=  (quotes are removed)
    if algo not in ALGOS:
        return jsonify(error='unknown algo', supported=list(ALGOS)), 400
    try:
        step = int(request.args.get('step', ''))                       # ?step=
        n_max = int(request.args.get('n_max', '').replace(',', ''))    # ?n_max=  (10,000 works too)
    except ValueError:
        return jsonify(error='step and n_max must be whole numbers'), 400
    if step < 1 or n_max < 0:
        return jsonify(error='step must be at least 1 and n_max at least 0'), 400
    if n_max // step > 5000:                                           # protects against huge requests
        return jsonify(error='too many points, use a bigger step or a smaller n_max'), 400

    sizes, times, fig = time_complexity_visualizer(ALGOS[algo], 0, n_max, step)   # minimum is 0
    os.makedirs(PLOTS_DIR, exist_ok=True)
    path = os.path.join(PLOTS_DIR, f'{algo}_n{n_max}_step{step}.png')
    fig.savefig(path)                                      # save the image on this computer
    plt.close(fig)
    with open(path, 'rb') as f:
        image = base64.b64encode(f.read()).decode()        # image -> text for the JSON
    return jsonify(algo=algo, n_min=0, n_max=n_max, step=step, input_sizes=sizes,
                   times=times, image_path=path, image_base64=image)


if __name__ == '__main__':
    app.run(port=8000, threaded=False)   # localhost:8000, one request at a time so charts don't mix
