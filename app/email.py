import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Configurar chave API e remetente padrão
SENDINBLUE_API_KEY = os.getenv('SENDINBLUE_API_KEY')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'queisecarvalhodev@gmail.com')

if not SENDINBLUE_API_KEY:
    raise ValueError("A chave SENDINBLUE_API_KEY não está definida. Por favor, defina a variável de ambiente.")

# Configurar a API do Sendinblue
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = SENDINBLUE_API_KEY

# Instanciar a API de emails transacionais
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# Função para enviar email
def send_email(recipient, subject, body):
    sender = {"name": "Meu Diário Oficial", "email": MAIL_DEFAULT_SENDER}
    to = [{"email": recipient}]
    email = sib_api_v3_sdk.SendSmtpEmail(to=to, sender=sender, subject=subject, text_content=body)
    
    try:
        api_response = api_instance.send_transac_email(email)
        print(api_response)
        return api_response
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}")
        return None
