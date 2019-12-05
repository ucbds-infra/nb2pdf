############################################
##### Unit Tests for NB Cell Filtering #####
############################################

import unittest
from unittest import mock
import json
from nb2pdf.filter_cells import *
from nb2pdf.pdf import *
from nb2pdf import convert
import subprocess
import os

class TestCellFilter(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self._file = "test/test-nb.ipynb"
		with open("test/output.ipynb") as f:
			self._correct_output = json.load(f)

	def test_filter(self):
		output = load_and_filter(self._file)
		self.assertEqual(output, self._correct_output)

class TestPDFIsExported(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self._file = "test/test-nb.ipynb"
		self._output_path = "test/test-nb.pdf"

	def test_pdf_exists(self):
		convert(self._file)
		self.assertTrue(os.path.exists(self._output_path) and \
			os.path.isfile(self._output_path))

	@classmethod
	def tearDownClass(self):
		remove = ["rm", "-f", self._output_path]
		subprocess.run(remove)