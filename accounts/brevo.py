import requests
from django.conf import settings

BREVO_URL = "https://api.brevo.com/v3/smtp/email"

def send_brevo_email(subject, html_content, to_email, to_name=None):
    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": "Link Lovers",
            "email": "linkloversng@gmail.com",  # MUST be verified in Brevo
        },
        "to": [
            {
                "email": to_email,
                "name": to_name or to_email,
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
    }

    try:
        response = requests.post(
            BREVO_URL,
            headers=headers,
            json=payload,
            timeout=10,  # important
        )

        response.raise_for_status()
        return True

    except requests.RequestException as e:
        print("Brevo API email failed:", e)
        return False
