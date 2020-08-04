##########################################
##### IPYNB to PDF Conversion Script #####
##########################################

import nbformat
import json
from io import StringIO
from nbpdfexport import notebook_to_pdf
import asyncio
from .asyncio_patch import monkeypatch, run_nested_until_complete


def export_to_pdf(notebook, pdf_name):
    """
    Export a notebook as a pdf.
    Args:
        notebook: json object / dictionary version of notebook to convert.
        pdf_name: name of outputted pdf
    """

    try:
        version = notebook["nbformat"]
    except KeyError:
        version = 4

    notebook_model = nbformat.read(StringIO(json.dumps(notebook)), as_version = version)

    try:
        __IPYTHON__
        run_nested_until_complete(notebook_to_pdf(notebook_model, pdf_name))
    except NameError:
        asyncio.get_event_loop().run_until_complete(notebook_to_pdf(notebook_model, pdf_name))
