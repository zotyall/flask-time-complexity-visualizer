# Run the tests:  python -m unittest -v
import base64
import os
import shutil
import tempfile
import unittest

import app as app_module
from algorithms import (ALGOS, bubble_sort, selection_sort, insertion_sort,
                        merge_sort, quick_sort)


class SortTests(unittest.TestCase):
    def test_sorts_really_sort(self):
        # the input is a reversed list, so a correct sort gives [1, 2, ..., 50]
        for sort in (bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort):
            self.assertEqual(sort(50), list(range(1, 51)), sort.__name__)

    def test_at_least_four_algorithms(self):
        for name in ('linear_search', 'bubble_sort', 'binary_search', 'nested_loops'):
            self.assertIn(name, ALGOS)


class AnalyzeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()            # images from tests go to a temp folder
        app_module.PLOTS_DIR = self.tmp
        self.client = app_module.app.test_client()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def analyze(self, query):
        return self.client.get('/analyze?' + query)

    def test_every_algorithm_works(self):
        for name in ALGOS:
            r = self.analyze(f'algo={name}&step=20&n_max=100')
            self.assertEqual(r.status_code, 200, name)
            data = r.get_json()
            self.assertEqual(data['input_sizes'], [0, 20, 40, 60, 80, 100], name)   # minimum is 0
            self.assertEqual(len(data['times']), 6, name)

    def test_image_is_saved_and_in_json(self):
        data = self.analyze('algo=linear_search&step=10&n_max=50').get_json()
        self.assertTrue(os.path.exists(data['image_path']))                          # saved locally
        self.assertEqual(base64.b64decode(data['image_base64'])[:4], b'\x89PNG')     # base64 is a real PNG

    def test_assignment_example_url(self):
        r = self.analyze("algo='linear_search'&step=10&n_max=10,000")                # quotes and comma
        data = r.get_json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(data['input_sizes'][-1], 10000)
        self.assertEqual(len(data['input_sizes']), 1001)

    def test_bad_input_gives_400(self):
        self.assertEqual(self.analyze('algo=nope&step=10&n_max=100').status_code, 400)
        self.assertEqual(self.analyze('algo=bubble_sort&step=0&n_max=100').status_code, 400)
        self.assertEqual(self.analyze('algo=bubble_sort&step=abc&n_max=100').status_code, 400)
        self.assertEqual(self.analyze('algo=bubble_sort&n_max=100').status_code, 400)
        self.assertEqual(self.analyze('algo=bubble_sort&step=1&n_max=999999999').status_code, 400)

    def test_home_page(self):
        self.assertEqual(self.client.get('/').status_code, 200)


if __name__ == '__main__':
    unittest.main()
