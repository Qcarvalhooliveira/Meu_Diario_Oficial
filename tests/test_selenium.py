from app.utils import download_pdf, extract_text_from_pdf 
import io

def test_download_pdf():
    url = 'http://www.dom.salvador.ba.gov.br/'
    pdf_file = download_pdf(url)
    assert pdf_file is not None
    assert isinstance(pdf_file, io.BytesIO)

    text = extract_text_from_pdf(pdf_file)

    keyword = "EULINA SANTOS SANTANA"
    # verificar como se comporta com linhas quebradas. para entender como fazer para ele encontrar o keyword
    keyword_lower = keyword.lower()
    text_normalized = ' '.join(text.lower().split())

    start_pos = text_normalized.find(keyword_lower)

    if start_pos != -1:
        # Imprimir um contexto de 50 caracteres antes e depois da palavra encontrada
        context_start = max(start_pos - 50, 0)
        context_end = min(start_pos + len(keyword) + 50, len(text))
        match_context = text[context_start:context_end]
        print(f"Match encontrado para a palavra '{keyword}': ...{match_context}...")
    else:
        print(f"Nenhum match encontrado para a palavra '{keyword}'")
    
    assert start_pos != -1

   
test_download_pdf()
