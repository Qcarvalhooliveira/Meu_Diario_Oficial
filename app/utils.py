import requests
from PyPDF2 import PdfFileReader
import io

def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        raise Exception('Failed to download PDF')

def extract_text_from_pdf(pdf_file):
    pdf = PdfFileReader(pdf_file)
    text = ""
    for page_num in range(pdf.numPages):
        page = pdf.getPage(page_num)
        text += page.extract_text()
    return text
