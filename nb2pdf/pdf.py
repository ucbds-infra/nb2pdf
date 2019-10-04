import nbformat
from nbconvert import PDFExporter
import json
from io import StringIO


def export_to_pdf(notebook, pdf_name):
    """
    Export a notebook as a pdf.
    Args:
        notebook: json object / dictionary version of notebook to convert.
        pdf_name: name of outputted pdf
    """
    pdf_exporter = PDFExporter()

    pdf_data, resources = pdf_exporter.from_file(StringIO(json.dumps(notebook)))

    with open(pdf_name, "wb") as f:
        f.write(pdf_data)
