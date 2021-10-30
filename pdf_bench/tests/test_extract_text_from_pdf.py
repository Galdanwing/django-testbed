import pytest
import pdfplumber
import os
import tika
from tika import parser
import pikepdf
from PyPDF2 import PdfFileReader


def test_extract_text_with_pdfplumber():
    with pdfplumber.open("pdf_bench/pdf_files/sample.pdf") as pdf:
        assert pdf.pages[0].extract_text().strip().startswith("A Simple PDF File")


def test_extract_text_with_tika():
    assert parser.from_file("pdf_bench/pdf_files/sample.pdf")["content"].strip().startswith("A Simple PDF File")


def test_extract_text_with_pikepdf():
    # Currently implemented, but recommended against by pikepdf themselves.
    # with pikepdf.open("pdf_bench/pdf_files/sample.pdf") as pdf:
    ...


def test_extract_text_with_pypdf2():
    # The text gathered from this pdf does not include the "A" at the start.
    assert PdfFileReader("pdf_bench/pdf_files/sample.pdf").getPage(1).extractText().strip().startswith(
        "Simple PDF File")
