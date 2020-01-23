##################################
##### IPYNB to PDF Converter #####
##################################

from .filter_cells import *
from .pdf import *

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

	if dest is  None:
		pdf_path = path[:-5] + "pdf"
	else:
		pdf_path = dest

	if filtering:
		notebook = load_and_filter(path, filter_type=filter_type)
	else:
		notebook = load_notebook(path)
		
	export_to_pdf(notebook, pdf_path)