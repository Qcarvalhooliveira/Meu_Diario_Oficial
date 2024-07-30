import pytest
from app.utils import download_pdf, extract_text_from_pdf
from app.models import Subscription
from app import db, create_app
import io

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/Meu_Diario_Oficial.db'  # Certifique-se de que o banco de dados correto está sendo usado

    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def init_database(test_client):
    # Assumindo que já existem dados no banco de dados, não precisamos adicionar nada aqui.
    # Se precisar, você pode adicionar dados de teste aqui.
    pass

def test_download_pdf(init_database):
    # Obter todas as keywords reais do banco de dados
    subscriptions = Subscription.query.all()
    assert len(subscriptions) > 0, "No subscriptions found in the database."

    url = 'http://www.dom.salvador.ba.gov.br/'
    pdf_file = download_pdf(url)
    assert pdf_file is not None
    assert isinstance(pdf_file, io.BytesIO)

    text = extract_text_from_pdf(pdf_file)
    text_normalized = ' '.join(text.lower().split())

    for subscription in subscriptions:
        keyword = subscription.keyword
        keyword_lower = keyword.lower()

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

if __name__ == "__main__":
    pytest.main()
