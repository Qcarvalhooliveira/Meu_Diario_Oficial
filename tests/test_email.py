import pytest
from unittest.mock import patch
from app.email import send_email, generate_welcome_email, generate_notification_email, generate_error_email
import sib_api_v3_sdk

def test_send_email():
    """
    Test the send_email function to ensure it correctly constructs and sends an email.
    """
    with patch('sib_api_v3_sdk.TransactionalEmailsApi.send_transac_email') as mock_send_email:
        recipient = 'test@example.com'
        subject = 'Test Subject'
        body = '<p>This is a test email.</p>'

        send_email(recipient, subject, body)

        mock_send_email.assert_called_once()
        args, kwargs = mock_send_email.call_args
        email_arg = args[0]

        assert email_arg.to == [{"email": recipient}]
        assert email_arg.sender == {"name": "Meu Diário Oficial", "email": "meu.diario.oficial.ssa@gmail.com"}
        assert email_arg.subject == subject
        assert email_arg.html_content == body

def test_generate_welcome_email():
    """
    Test the generate_welcome_email function to ensure the generated HTML content is correct.
    """
    user_name = "John Doe"
    logo_url = "http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png"
    
    expected_email_body = f"""
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

    generated_email_body = generate_welcome_email(user_name, logo_url)
    
    assert generated_email_body.strip() == expected_email_body.strip()

def test_generate_notification_email():
    """
    Test the generate_notification_email function to ensure the generated HTML content is correct.
    """
    user_name = "Jane Doe"
    logo_url = "http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png"
    
    expected_email_body = f"""
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

    generated_email_body = generate_notification_email(user_name, logo_url)
    
    assert generated_email_body.strip() == expected_email_body.strip()

def test_generate_error_email():
    """
    Test the generate_error_email function to ensure the generated HTML content is correct.
    """
    user_name = "John Doe"
    logo_url = "http://www.dom.salvador.ba.gov.br/images/stories/logo_diario.png"
    
    expected_email_body = f"""
    <html>
    <body style="background-color: #ffff; font-family: Arial, sans-serif; margin: 0; padding: 0; width: 100%;">
        <div style="background-color: #c7e6fd; padding: 20px; text-align: center;">
            <table align="center" width="100%" style="max-width: 600px; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
                <tr>
                    <td style="text-align: center;">
                        <img src="{logo_url}" alt="Logo" style="margin: 0 0 30px 5px">
                        <h1 style="color: #333333; text-align: left; font-size: 20px; margin: 5px 0;">Atenção, {user_name}!</h1>
                        <p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">Falha na Verificação do Diário Oficial!</p>
                        <p style="color: #333333;text-align: left; font-size: 18px; margin: 5px 0;">
                         Houve uma falha ao tentar verificar o Diário Oficial de Salvador.
                         Por favor, verifique manualmente no site para mais detalhes.
                        </p>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """

    generated_email_body = generate_error_email(user_name, logo_url)
    
    assert generated_email_body.strip() == expected_email_body.strip()
