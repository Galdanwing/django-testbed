from datetime import datetime
from pathlib import Path

import fitz
import pdfplumber
import pdftotext
import psutil
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError
from pandas import DataFrame
from pdfminer.high_level import extract_text
from rich import print
from tika import parser

from pdf_bench.util import now


def check_speed_pdfplumber(amount: int, file: Path):
    starting_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    start_time = now()
    memory_usage = []
    for i in range(0, amount):
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                _ = page.extract_text()
                memory_usage.append(psutil.Process().memory_info().rss / (1024 * 1024) - starting_memory)
    return (now() - start_time).total_seconds() / amount, max(memory_usage)


def check_speed_pdfminer(amount: int, file: Path):
    starting_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    start_time = now()
    memory_usage = []
    for i in range(0, amount):
        with open(file, "rb") as pdf:
            _ = extract_text(pdf)
            memory_usage.append(psutil.Process().memory_info().rss / (1024 * 1024) - starting_memory)
    return (now() - start_time).total_seconds() / amount, max(memory_usage)


def check_speed_tika(amount: int, file: Path):
    starting_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    start_time = now()
    memory_usage = []

    for i in range(0, amount):
        _ = parser.from_file(str(file))["content"]
        memory_usage.append(psutil.Process().memory_info().rss / (1024 * 1024) - starting_memory)

    return (now() - start_time).total_seconds() / amount, max(memory_usage)


def check_speed_pypdf(amount: int, file: Path):
    starting_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    start_time = now()
    memory_usage = []
    for i in range(0, amount):
        pypdf_pdf = PdfFileReader(str(file))
        for page in pypdf_pdf.pages:
            _ = page.extractText()
            memory_usage.append(psutil.Process().memory_info().rss / (1024 * 1024) - starting_memory)
    return (now() - start_time).total_seconds() / amount, max(memory_usage)


def check_speed_pdftotext(amount: int, file: Path):
    starting_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    start_time = now()
    memory_usage = []
    for i in range(0, amount):
        with open(file, "rb") as pdf:
            for page in pdftotext.PDF(pdf):
                _ = page
                memory_usage.append(psutil.Process().memory_info().rss / (1024 * 1024) - starting_memory)
    return (now() - start_time).total_seconds() / amount, max(memory_usage)


def check_speed_mupdf(amount: int, file: Path):
    starting_memory = psutil.Process().memory_info().rss / (1024 * 1024)
    start_time = datetime.now()
    memory_usage = []
    for i in range(0, amount):
        with fitz.open(file) as doc:
            for page in doc:
                _ = page.get_text("text")
                memory_usage.append(psutil.Process().memory_info().rss / (1024 * 1024) - starting_memory)
    return (now() - start_time).total_seconds() / amount, max(memory_usage)


def check_speed_of_extracting_all_text(amount: int = 1):
    files = [
        Path("pdf_files/sample-small-text-only.pdf"),
        Path("pdf_files/intro-linux.pdf"),
        Path("pdf_files/pdf_with_svg_image.pdf"),
    ]
    overall_speed = {}
    overall_memory_usage = {}
    for i, file in enumerate(files):
        pdfplumber_speed, pdfplumber_memory_usage = check_speed_pdfplumber(amount, file)
        tika_speed, tika_memory_usage = check_speed_tika(amount, file)
        try:
            pypdf_speed, pypdf_memory_usage = check_speed_pypdf(amount, file)
        except PdfReadError:
            pypdf_speed = pypdf_memory_usage = "Error"
        pdfminer_speed, pdfminer_memory_usage = check_speed_pdfminer(amount, file)
        pdftotext_speed, pdftotext_memory_usage = check_speed_pdftotext(amount, file)
        mupdf_speed, mupdf_memory_usage = check_speed_mupdf(amount, file)
        speed = {
            "pdfminer": pdfminer_speed,
            "pdfplumber": pdfplumber_speed,
            "pypdf": pypdf_speed,
            "tika": tika_speed,
            "pdftotext": pdftotext_speed,
            "mupdf_speed": mupdf_speed,
        }
        memory_usage = {
            "pdfminer": pdfminer_memory_usage,
            "pdfplumber": pdfplumber_memory_usage,
            "pypdf": pypdf_memory_usage,
            "tika": tika_memory_usage,
            "pdftotext": pdftotext_memory_usage,
            "mupdf_speed": mupdf_memory_usage,
        }
        overall_speed[f"{file.stem}"] = speed
        overall_memory_usage[f"{file.stem}"] = memory_usage

        print(
            f"Current iteration counter {i}, current file {file=} current file {speed=} current_file {memory_usage=}")

    return DataFrame.from_dict(overall_speed), DataFrame.from_dict(overall_memory_usage)


def check_processing_speed():
    """
    Check speed of various operations within pdf.
    :return:
    """

    overall_speed, overall_memory_usage = check_speed_of_extracting_all_text()
    print("Overall speed in seconds")
    print(overall_speed.to_markdown())
    print("Overall memory usage in megabytes")
    print(overall_memory_usage.to_markdown())
