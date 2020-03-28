##################################
##### IPYNB to PDF Converter #####
##################################

import argparse
import os
import time

from IPython import get_ipython
from IPython.display import display

from .filter_cells import *
from .pdf import *

# check for IPython
IN_IPYTHON = get_ipython() is not None

def force_checkpoint():
	"""
	If in a Jupyter environment, force-saves notebook
	"""
	from IPython.core.magics.display import Javascript
	display(Javascript('''
        require(["base/js/namespace"], function() {
			Jupyter.notebook.save_notebook();
		});
    '''))
	time.sleep(0.5)

def convert(path, dest=None, filtering=False, filter_type="html"):
	"""
	Converts IPYNB file at PATH to PDF
	Args:
		path: Path to the IPYNB file
		dest: (optional) Output path
		filtering: (optional) whether or not to filter the
			notebook cells
		filter_type: (optional) how to filter the notebook, using
			HTML comments or cell tags; "html" or "tags"
	"""
	assert filter_type in ["html", "tags"], "{} is not a valid filter type".format(filter_type)

	if IN_IPYTHON:
		force_checkpoint()

	if dest is  None:
		pdf_path = path[:-5] + "pdf"
	else:
		pdf_path = dest

	if filtering:
		notebook = load_and_filter(path, filter_type=filter_type)
	else:
		notebook = load_notebook(path)
		
	export_to_pdf(notebook, pdf_path)

def cli():
	"""Command-Line Interface for nb2pdf"""
	parser = argparse.ArgumentParser()
	parser.add_argument("files", nargs="*", help="Files to convert")
	parser.add_argument("--tag-filter", default=False, help="Filter using tags", action="store_true")
	parser.add_argument("--html-filter", default=False, help="Filter using HTML comments", action="store_true")
	args = parser.parse_args()

	assert sum([args.tag_filter, args.html_filter]) <= 1, "Cannot filter using both HTML comments and tags"

	for file in args.files:
		assert os.path.exists(file) and os.path.isfile(file), "{} does not exist or is not a file".format(file)
		assert file[-6:] == ".ipynb", "{} is not an IPYNB file".format(file)

		convert(file, filtering = args.tag_filter or args.html_filter, filter_type = ("html", "tags")[args.tag_filter])
	