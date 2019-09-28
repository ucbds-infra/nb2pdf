############################################
##### Unit Tests for NB Cell Filtering #####
############################################

import unittest
import json
from nb2pdf.filter_cells import *

class TestCellFilter(unittest.TestCase):
	def setUp(self):
		self._file = "test/test-nb.ipynb"
		with open("test/output.ipynb") as f:
			self._correct_output = json.load(f)

	def test_filter(self):
		output = load_and_filter(self._file)
		self.assertEqual(output, self._correct_output)