import pytest
from app.utils import download_pdf, extract_text_from_pdf
from app.models import Subscription, User
from app import db, create_app
import io

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/Meu_Diario_Oficial.db'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()

@pytest.fixture(scope='function')
def init_database(test_client):
    with test_client.application.app_context():
        db.create_all()
        user1 = User(name='Test User 1', email='queisecarvalho@hotmail.com')
        user2 = User(name='Test User 2', email='iurithauront@gmail.com')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        subscription1 = Subscription(user_id=user1.id, keyword='test keyword 1')
        subscription2 = Subscription(user_id=user2.id, keyword='test keyword 2')
        db.session.add(subscription1)
        db.session.add(subscription2)
        db.session.commit()

        yield db
        db.session.remove()
        db.drop_all()

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
