from email.message import EmailMessage
import smtplib, ssl
from typing import Optional
from ..settings import settings

def send_email_stub(shelter_name: str, intake_req):
    print(f"[NOTIFY] Shelter '{shelter_name}' received new intake request:")
    print(f" - Name: {intake_req.name or 'N/A'}")
    print(f" - Reason: {intake_req.reason or 'N/A'}")
    print(f" - ETA: {intake_req.eta or 'unspecified'}")

def send_email_intake(shelter_name: str, intake_req, to_email: Optional[str] = None):
    """
    Sends a real email if EMAIL_ENABLED=True; otherwise prints to console.
    Falls back to stub on any exception so it never blocks the request.
    """
    if not settings.EMAIL_ENABLED:
        return send_email_stub(shelter_name, intake_req)

    msg = EmailMessage()
    msg["Subject"] = f"[Shelter App] New intake request for {shelter_name}"
    msg["From"] = settings.EMAIL_FROM or settings.SMTP_USER
    msg["To"] = to_email or settings.EMAIL_TO_DEFAULT or settings.SMTP_USER

    body = (
        f"New intake request for {shelter_name}\n\n"
        f"Name: {intake_req.name or 'N/A'}\n"
        f"Reason: {intake_req.reason or 'N/A'}\n"
        f"ETA: {intake_req.eta or 'unspecified'}\n"
        f"Intake ID: {intake_req.id}\n"
    )
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
            if settings.SMTP_STARTTLS:
                server.starttls(context=context)
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        print(f"[EMAIL] Sent intake notification to {msg['To']}")
    except Exception as e:
        print(f"[EMAIL][ERROR] {e}. Falling back to stub.")
        send_email_stub(shelter_name, intake_req)
