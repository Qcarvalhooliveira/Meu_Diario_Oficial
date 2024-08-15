import pytest
from app.utils import download_pdf, extract_text_from_pdf
from app.models import User
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
        user1 = User(id='user1', name='BRUNO SOARES REIS', email='doc.test.id4@gmail.com')
        user1.set_password('password1')
        user2 = User(id='user2', name='LUIZ ANTÔNIO VASCONCELLOS CARREIRA', email='zara.test.id2@gmail.com')
        user2.set_password('password2')
        db.session.add_all([user1, user2])
        db.session.commit()

        yield db
        db.session.remove()
        db.drop_all()

def test_download_pdf(init_database):
    # Obter todos os nomes reais dos usuários no banco de dados
    users = User.query.all()
    assert len(users) > 0, "No users found in the database."

    url = 'http://www.dom.salvador.ba.gov.br/'
    pdf_file = download_pdf(url)
    assert pdf_file is not None
    assert isinstance(pdf_file, io.BytesIO)

    text = extract_text_from_pdf(pdf_file)
    text_normalized = ' '.join(text.lower().split())

    for user in users:
        user_name = user.name
        user_name_lower = user_name.lower()

        start_pos = text_normalized.find(user_name_lower)

        if start_pos != -1:
            # Imprimir um contexto de 50 caracteres antes e depois da palavra encontrada
            context_start = max(start_pos - 50, 0)
            context_end = min(start_pos + len(user_name) + 50, len(text))
            match_context = text[context_start:context_end]
            print(f"Match encontrado para o nome '{user_name}': ...{match_context}...")
        else:
            print(f"Nenhum match encontrado para o nome '{user_name}'")
        
        assert start_pos != -1

if __name__ == "__main__":
    pytest.main()
