from email.message import EmailMessage
import smtplib, ssl
from typing import Optional, TYPE_CHECKING
from ..settings import settings

if TYPE_CHECKING:
    from twilio.rest import Client

# Optional Twilio import guarded so imports don't crash if not installed
try:
    from twilio.rest import Client as TwilioClient  # runtime alias
except Exception:  # pragma: no cover
    TwilioClient = None

# Email notifications
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

# SMS notifications
def _twilio_client() -> Optional["Client"]:
    if not settings.TWILIO_ENABLED:
        print("[SMS] TWILIO_ENABLED is false; skipping SMS send.")
        return None
    if TwilioClient is None:
        print("[SMS][ERROR] Twilio SDK not installed. `pip install twilio`")
        return None
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        print("[SMS][ERROR] Missing TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN.")
        return None
    return TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)


def send_sms_twilio(
    body: str,
    to_number: str,
    *,
    from_number: Optional[str] = None,
    messaging_service_sid: Optional[str] = None,
) -> None:
    """
    Generic Twilio SMS sender. Uses Messaging Service SID if provided;
    otherwise uses a From number. Safe: logs errors and returns.
    """
    client = _twilio_client()
    if not client:
        return

    # Prefer explicit args, then settings, then error
    ms_sid = (
        messaging_service_sid
        or getattr(settings, "TWILIO_MESSAGING_SERVICE_SID", "")  # may be empty
        or None
    )
    from_num = from_number or settings.TWILIO_FROM_NUMBER or None

    try:
        kwargs = {"to": to_number, "body": body}
        if ms_sid:
            kwargs["messaging_service_sid"] = ms_sid
        elif from_num:
            kwargs["from_"] = from_num
        else:
            print("[SMS][ERROR] No Messaging Service SID or From number configured.")
            return

        msg = client.messages.create(**kwargs)
        print(f"[SMS] Sent to {to_number}; sid={msg.sid}")
    except Exception as e:
        print(f"[SMS][ERROR] {e}")


def send_intake_sms(shelter_name: str, intake_req, to_number: str) -> None:
    """
    Formats an intake alert and sends via Twilio SMS.
    """
    body = (
        f"New intake at {shelter_name}\n"
        f"Name: {intake_req.name or 'N/A'}\n"
        f"Reason: {intake_req.reason or 'N/A'}\n"
        f"ETA: {intake_req.eta or 'unspecified'}\n"
        f"Intake ID: {intake_req.id}"
    )
    send_sms_twilio(body, to_number)

def send_intake_status_sms(shelter, intake_req) -> None:
    """
    Sends an SMS to the requester (for now: default test destination) whenever
    an intake status changes. Includes shelter info and the new status.
    """
    to_number = getattr(settings, "TEST_SMS_TO", "")
    if not to_number:
        print("[SMS] No TEST_SMS_TO configured; skipping status SMS.")
        return

    body = (
        f"Update from {shelter.name}\n"
        f"Address: {shelter.address}\n\n"
        f"Intake status is now: {intake_req.status}\n"
        f"Name: {intake_req.name or 'N/A'}\n"
        f"Reason: {intake_req.reason or 'N/A'}\n"
        f"ETA: {intake_req.eta or 'unspecified'}\n"
        f"Intake ID: {intake_req.id}"
    )
    send_sms_twilio(body, to_number)
