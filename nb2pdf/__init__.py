##################################
##### IPYNB to PDF Converter #####
##################################

from .filter_cells import *
from .pdf import *

def convert(path):
	"""Converts IPYNB file at PATH to PDF"""
	notebook = load_and_filter(path)
	export_to_pdf(notebook, path[:-5] + "pdf")