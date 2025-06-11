import zipfile
import csv
import io
import openpyxl
import PyPDF2
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RESOURCE_DIR = os.path.join(BASE_DIR, 'resources')
ZIP_PATH = os.path.join(RESOURCE_DIR, 'wedding_files.zip')


def test_zip_contains_all_files():
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        files = zf.namelist()
        assert set(files) == {"sample.pdf", "sample.xlsx", "sample.csv"}


def test_csv_content():
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        with zf.open("sample.csv") as f:
            reader = csv.reader(io.TextIOWrapper(f, encoding='utf-8'))
            rows = list(reader)
            assert rows[1][0] == "Анна и Иван"


def test_xlsx_content():
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        with zf.open("sample.xlsx") as f:
            wb = openpyxl.load_workbook(io.BytesIO(f.read()))
            sheet = wb.active
            assert sheet['A2'].value == "Анна и Иван"


def test_pdf_contains_name():
    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        with zf.open("sample.pdf") as f:
            reader = PyPDF2.PdfReader(f)
            text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
            assert "2025-07-12" in text, f"Expected date not found in PDF text:\n{text}"
