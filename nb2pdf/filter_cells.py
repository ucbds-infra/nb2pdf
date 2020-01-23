################################################
##### Cell Filtering for Jupyter Notebooks #####
################################################

import json
import re

_BEGIN_QUESTION_REGEX = r"<!-- BEGIN QUESTION (.* )?-->"
_END_QUESTION_REGEX = r"<!-- END QUESTION (.* )?-->"

def load_notebook(nb_path):
	with open(nb_path) as f:
		notebook = json.load(f)
	return notebook

def load_and_filter(nb_path, filter_type):
	notebook = load_notebook(nb_path)
	filter_fn = {
		"tags": filter_notebook_cells_by_tag,
		"html": filter_notebook_cells_by_comments,
	}[filter_type]
	return filter_fn(notebook)

def filter_notebook_cells_by_comments(notebook):
	cells = notebook["cells"]
	curr_idx, idx_to_delete, in_question = 0, [], False
	for cell in cells:
		line_idx, lines_before_begin, lines_after_end = 0, -1, -1
		for line in cell["source"]:
			if not in_question:
				# check for begin question regex in source
				match = re.search(_BEGIN_QUESTION_REGEX, line)
				if match and lines_before_begin == -1:
					lines_before_begin = line_idx
					in_question = True
			else:
				# check for end question regex in source
				match = re.search(_END_QUESTION_REGEX, line)
				if match:
					lines_after_end = line_idx
					in_question = False
			line_idx += 1

		# if we are not in question and there is no begin/end comment, delete the cell
		if lines_before_begin == -1 and lines_after_end == -1 and not in_question:
			idx_to_delete += [curr_idx]

		# if there is an end comment, delete lines after that
		if lines_after_end != -1:
			del cell["source"][lines_after_end+1:]

		# if there is a begin comment, delete lines before that
		if lines_before_begin != -1:
			del cell["source"][:lines_before_begin]

		curr_idx += 1
	
	# reverse indices list so that we do not need to decrement while deleting
	idx_to_delete.reverse()

	# delete at indices
	for idx in idx_to_delete:
		del cells[idx]

	return notebook

		


def filter_notebook_cells_by_tag(notebook):
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
