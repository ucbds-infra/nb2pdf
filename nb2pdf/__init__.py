##################################
##### IPYNB to PDF Converter #####
##################################

from .filter_cells import *

def convert(path):
	"""Converts IPYNB file at PATH to PDF"""
	notebook = load_and_filter(path)
	# TODO: Add in PDF conversion
	return None # TODO: set return value