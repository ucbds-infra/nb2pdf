# Jupyter Notebook to PDF Converter

This package is a converter for IPYNB files to PDFs that runs on nbconvert and pandoc. This package was built for use in [otter-grader](https://github.com/ucbds-infra/otter-grader), an open-source local autograding framework.

Because this converter was designed for an autograding library, it has some import [caveats](#Cell-Filtering) about how it generates PDFs, most importantly concerning how it filters cells. **This library is not meant to be a wrapper for nbconvert, as it has filtering behaviors that will exclude several cells by default.**

## Installation

nb2pdf is installed via pip:

```
pip install nb2pdf
```

### Dependencies

Because this package uses nbconvert to convert IPYNB files to PDFs, it requires pandoc and xetex to be installed. 

## Usage

The nb2pdf API is very simple, and is encapsulated in a single function: `nb2pdf.convert`. This function  will convert the IPYNB file at the path passed to it as an argument to a PDF file in the same directory:

```python
from nb2pdf import convert
convert("/path/to/your/notebook.ipynb")
```

### Cell Filtering

This convert, which is designed to generate manual-graded PDF submissions for autograders, defaults to a few filtering behaviors. The only cells kept in the output are those that fall into one of the three categories below:

* Markdown cells
* Cells with images in the output
* Cells tagged `include`

The converter removes code cells with no images in the output, as it is assumed that these cells will be autograded. To include cells that _do not_ fall into either of the first two categories, tag these cells with `include` to keep them in the output. Similarly, to exclude cells that _do_ fall into the first two categories, tag them with `ignore`.