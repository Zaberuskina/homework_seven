import zipfile
import os
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RESOURCE_DIR = os.path.join(BASE_DIR, 'resources')
ZIP_PATH = os.path.join(RESOURCE_DIR, 'wedding_files.zip')

PDF_PATH = os.path.join(RESOURCE_DIR, 'sample.pdf')
XLSX_PATH = os.path.join(RESOURCE_DIR, 'sample.xlsx')
CSV_PATH = os.path.join(RESOURCE_DIR, 'sample.csv')


@pytest.fixture(scope="module", autouse=True)
def create_zip():
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    with zipfile.ZipFile(ZIP_PATH, 'w') as zf:
        zf.write(PDF_PATH, arcname="sample.pdf")
        zf.write(XLSX_PATH, arcname="sample.xlsx")
        zf.write(CSV_PATH, arcname="sample.csv")

    yield

    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)
