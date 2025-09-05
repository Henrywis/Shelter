def send_email_stub(shelter_name: str, intake_req):
    # In real app, use SendGrid, SES, or SMTP.
    print(f"[NOTIFY] Shelter '{shelter_name}' received new intake request:")
    print(f" - Name: {intake_req.name or 'N/A'}")
    print(f" - Reason: {intake_req.reason or 'N/A'}")
    print(f" - ETA: {intake_req.eta or 'unspecified'}")
