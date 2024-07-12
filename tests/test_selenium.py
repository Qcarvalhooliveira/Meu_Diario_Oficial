from app.utils import download_pdf
import io

def test_download_pdf():
    url = 'http://www.dom.salvador.ba.gov.br/'
    pdf_file = download_pdf(url)
    assert pdf_file is not None
    assert isinstance(pdf_file, io.BytesIO)

test_download_pdf()
