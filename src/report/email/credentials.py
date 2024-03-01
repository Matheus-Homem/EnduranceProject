import os
from dotenv import load_dotenv
from dataclasses import dataclass

@dataclass
class Credentials:
	USERNAME: str
	PASSWORD: str
	PORT: int
	SERVER: str
	RECIPIENT: str
	VALIDATED_EMAIL: str


load_dotenv()
credentials = Credentials(
	USERNAME=os.getenv("SMTP_USERNAME"),
	PASSWORD=os.getenv("SMTP_PASSWORD"),
	PORT=587,
	SERVER="smtp.gmail.com",
	RECIPIENT=os.getenv("SMTP_RECIPIENT"),
	VALIDATED_EMAIL=os.getenv("VERIFIED_EMAIL")
)
