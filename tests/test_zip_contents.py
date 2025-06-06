import zipfile
import csv
import io
import openpyxl
import PyPDF2
import os

RESOURCE_DIR = os.path.join(os.path.dirname(__file__), '../resources')
ZIP_PATH = os.path.join(RESOURCE_DIR, 'wedding_files.zip')

PDF_PATH = os.path.join(RESOURCE_DIR, 'sample.pdf')
XLSX_PATH = os.path.join(RESOURCE_DIR, 'sample.xlsx')
CSV_PATH = os.path.join(RESOURCE_DIR, 'sample.csv')


def test_create_zip_from_existing_files():
    with zipfile.ZipFile(ZIP_PATH, 'w') as zf:
        zf.write(PDF_PATH, arcname="sample.pdf")
        zf.write(XLSX_PATH, arcname="sample.xlsx")
        zf.write(CSV_PATH, arcname="sample.csv")
    assert os.path.exists(ZIP_PATH)


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
