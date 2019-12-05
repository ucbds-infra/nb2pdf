################################################
##### Cell Filtering for Jupyter Notebooks #####
################################################

import json

def load_notebook(nb_path):
	with open(nb_path) as f:
		notebook = json.load(f)
	return notebook

def load_and_filter(nb_path):
	notebook = load_notebook(nb_path)
	return filter_notebook_cells(notebook)

def filter_notebook_cells(notebook):
	cells = notebook["cells"]
	curr_idx, idx_to_delete = 0, []
	for cell in cells:
		# check if cell is code & deletable
		if cell["cell_type"] == "code" and is_deletable_code(cell):
			idx_to_delete += [curr_idx]

		# check if cell is markdown & deletable
		elif cell["cell_type"] == "markdown" and is_deletable_markdown(cell):
			idx_to_delete += [curr_idx]

		curr_idx += 1

	# reverse indices list so that we do not need to decrement while deleting
	idx_to_delete.reverse()

	# delete at indices
	for idx in idx_to_delete:
		del cells[idx]

	return notebook

def is_deletable_code(cell):
	"""Returns whether or not cell is deletable"""
	# check if the "include" tag is in metadata
	if "tags" in cell["metadata"] and "include" in cell["metadata"]["tags"]:
		return False

	# check if the "ignore" tag is in metadata
	if "tags" in cell["metadata"] and "ignore" in cell["metadata"]["tags"]:
		return True

	# check if there is an image in the output
	elif len(cell["outputs"]) > 0:
		for output in cell["outputs"]:
			if "data" in output and "image/png" in output["data"]:
				return False

	# if neither of above is True, then cell is deletable
	return True

def is_deletable_markdown(cell):
	# check if the "ignore" tag is in metadata
	if "tags" in cell["metadata"] and "ignore" in cell["metadata"]["tags"]:
		return True
	return False
