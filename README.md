# Jupyter Notebook to PDF Converter

This package converst Jupyter Notebooks (`.ipynb` files) to PDFs using nbconvert. It is designed to create manual submissions for the [Python local grader](https://github.com/ucbds-infra/local-grader) being developed by the UC Berkeley Division of Data Science and Information.

## Usage

The converter by default leaves all cells alone but **removes** code cells without an image in the output. (This is designed to output graphs generated in notebooks in the PDF.) Using metadata tags, cells can be included (with the `include` tag) or excluded (with the `ignore` tag).