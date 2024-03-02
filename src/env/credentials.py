import os
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class Credentials:
	SMTP_PORT: int
	SMTP_SERVER: str
	SMTP_USERNAME: str
	SMTP_PASSWORD: str
	SMTP_RECIPIENT: str
	IMAP_SENDER: str
	IMAP_PASSWORD: str
	IMAP_RECIPIENT: str
	VALIDATED_EMAIL: str

load_dotenv()
credentials = Credentials(
	SMTP_PORT=587,
	SMTP_SERVER="smtp.gmail.com",
	SMTP_USERNAME=os.getenv("SMTP_USERNAME"),
	SMTP_PASSWORD=os.getenv("SMTP_PASSWORD"),
	SMTP_RECIPIENT=os.getenv("SMTP_RECIPIENT"),
	IMAP_SENDER=os.getenv("IMAP_SENDER"),
	IMAP_PASSWORD=os.getenv("IMAP_PASSWORD"),
	IMAP_RECIPIENT=os.getenv("IMAP_RECIPIENT"),
	VALIDATED_EMAIL=os.getenv("VERIFIED_EMAIL"),
)
