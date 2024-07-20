import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

SENDINBLUE_API_KEY = os.getenv('SENDINBLUE_API_KEY')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'seu_email@example.com')

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = SENDINBLUE_API_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_email(recipient, subject, body):
    sender = {"email": MAIL_DEFAULT_SENDER}
    to = [{"email": recipient}]
    email = sib_api_v3_sdk.SendSmtpEmail(to=to, sender=sender, subject=subject, text_content=body)
    
    try:
        api_response = api_instance.send_transac_email(email)
        return api_response
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        return None
