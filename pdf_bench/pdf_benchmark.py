from pathlib import Path

import pdfplumber
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError
from django.utils.timezone import now
from pdfminer.high_level import extract_text
from tika import parser
import pdftotext

from timeit import timeit


def check_correctness_of_results():
    """
    Check accuracy of pdf libraries through several operations
    :return:
    """

    def check_correctness_of_extracted_text():
        ...

    def check_correctness_of_tables():
        ...

    check_correctness_of_extracted_text()
    check_correctness_of_tables()


def check_speed_pdfplumber(amount: int, file: Path):
    start_time = now()
    for i in range(0, amount):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                _ = page.extract_text()
    return now() - start_time


def check_speed_pdfminer(amount: int, file: Path):
    start_time = now()
    for i in range(0, amount):
        with open(file, "rb") as pdf:
            _ = extract_text(pdf)
    return now() - start_time


def check_speed_tika(amount: int, file: Path):
    start_time = now()
    for i in range(0, amount):
        _ = parser.from_file(str(file))["content"]

    return now() - start_time


def check_speed_pypdf(amount: int, file: Path):
    start_time = now()
    for i in range(0, amount):
        pypdf_pdf = PdfFileReader(str(file))

        for page in pypdf_pdf.pages:
            _ = page.extractText()
    return now() - start_time


def check_speed_pdftotext(amount: int, file: Path):
    start_time = now()
    for i in range(0, amount):
        with open(file, "rb") as pdf:
            for page in pdftotext.PDF(pdf):
                _ = page
    return now() - start_time


def check_speed_of_extracting_all_text():
    files = [
        Path("pdf_bench/pdf_files/sample-small-text-only.pdf"),
        Path("pdf_bench/pdf_files/intro-linux.pdf"),
        Path("pdf_bench/pdf_files/pdf_with_svg_image.pdf"),
    ]
    amount = 5
    res = {}
    for file in files:
        try:
            pdfplumber_speed = (
                check_speed_pdfplumber(amount, file).total_seconds() / amount
            )
        except Exception:
            pdfplumber_speed = "Error"
        try:
            tika_speed = check_speed_tika(amount, file).total_seconds() / amount
        except Exception:
            tika_speed = "Error"
        try:
            pypdf_speed = check_speed_pypdf(amount, file).total_seconds() / amount
        except Exception:
            pypdf_speed = "Error"
        try:
            pdfminer_speed = check_speed_pdfminer(amount, file).total_seconds() / amount
        except Exception:
            pdfminer_speed = "Error"
        try:
            pdftotext_speed = (
                check_speed_pdftotext(amount, file).total_seconds() / amount
            )
        except Exception:
            pdftotext_speed = "Error"

        res[file.stem] = {
            "pdfminer": pdfminer_speed,
            "pdfplumber": pdfplumber_speed,
            "pypdf": pypdf_speed,
            "tika": tika_speed,
            "pdftotext": pdftotext_speed,
        }
    return res


def check_speed_of_results():
    """
    Check speed of various operations within pdf.
    :return:
    """

    check_speed_of_extracting_all_text()


def generate_benchmark():
    check_correctness_of_results()
    check_speed_of_results()
