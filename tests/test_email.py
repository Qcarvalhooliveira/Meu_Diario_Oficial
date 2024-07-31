import pytest
from unittest.mock import patch
from app.email import send_email
import sib_api_v3_sdk

def test_send_email():
    with patch('sib_api_v3_sdk.TransactionalEmailsApi.send_transac_email') as mock_send_email:
        recipient = 'queisecarvalhodev@gmail.com'
        subject = 'Test Subject'
        body = 'This is a test email.'

        send_email(recipient, subject, body)

        mock_send_email.assert_called_once()
        args, kwargs = mock_send_email.call_args
        email_arg = args[0]

        assert email_arg.to == [{"email": recipient}]
        assert email_arg.sender == {"name": "Meu Diário Oficial", "email": "queisecarvalhodev@gmail.com"}
        assert email_arg.subject == subject
        assert email_arg.text_content == body
