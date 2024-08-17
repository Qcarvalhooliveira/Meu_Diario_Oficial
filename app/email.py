import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Configurar chave API e remetente padrão
SENDINBLUE_API_KEY = os.getenv('SENDINBLUE_API_KEY')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'meu.diario.oficial.ssa@gmail.com')

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
    email = sib_api_v3_sdk.SendSmtpEmail(to=to, sender=sender, subject=subject, html_content=body)
    
    try:
        api_response = api_instance.send_transac_email(email)
        print(api_response)
        return api_response
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}")
        return None

def generate_welcome_email(user_name, logo_url):
    return f"""
    <html>
    <body style="background-color: #ffff; font-family: Arial, sans-serif; margin: 0; padding: 0; width: 100%;">
        <div style="background-color: #c7e6fd; padding: 20px; text-align: center;">
            <table align="center" width="100%" style="max-width: 600px; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td style="text-align: center;">
                        <img src="{logo_url}" alt="Logo" style="margin: 0 0 30px 5px">
                        <h1 style="color: #333333; text-align: left; font-size: 20px; margin: 5px 0;">Parabéns, {user_name}!</h1>
                        <p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">Seu e-mail foi cadastrado com sucesso em nossa aplicação.</p>
                        <p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">Estamos felizes em tê-lo(a) conosco!</p>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """

def generate_notification_email(user_name, logo_url):
    return f"""
    <html>
    <body style="background-color: #ffff; font-family: Arial, sans-serif; margin: 0; padding: 0; width: 100%;">
        <div style="background-color: #c7e6fd; padding: 20px; text-align: center;">
            <table align="center" width="100%" style="max-width: 600px; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td style="text-align: center;">
                        <img src="{logo_url}" alt="Logo" style="margin: 0 0 30px 5px">
                        <h1 style="color: #333333; text-align: left; font-size: 20px; margin: 5px 0;">Parabéns, {user_name}!</h1>
                        <p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">Seu nome foi encontrado no Diário Oficial de Salvador!</p>
                        <p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">
                            Por favor, verifique diretamente no site para qual concurso você foi convocado.
                        </p>
                        <p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">
                            Estamos torcendo por você!
                        </p>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """
