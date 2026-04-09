# src/pdf_writer.py

from fpdf import FPDF
import os

def save_pdf(text: str, path: str = "output/article.pdf") -> str:
    """
    Saves the given text as a PDF file.

    Args:
        text (str): The content to write to the PDF.
        path (str): Path where the PDF will be saved. Defaults to 'output/article.pdf'.

    Returns:
        str: The path of the saved PDF file.
    """
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Split text into lines and write to PDF
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    # Save PDF
    pdf.output(path)

    return path
