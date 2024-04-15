import os
from dataclasses import dataclass


@dataclass
class Credentials:
    SMTP_PORT: int = 587
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_USERNAME: str = os.getenv("SMTP_SENDER_EMAIL")
    SMTP_PASSWORD: str = os.getenv("SMTP_SENDER_PASSWORD")
    SMTP_RECIEVER: str = os.getenv("SMTP_RECIEVER_EMAIL")
    IMAP_SENDER: str = os.getenv("IMAP_SENDER")
    IMAP_PASSWORD: str = os.getenv("IMAP_PASSWORD")
    IMAP_RECIEVER: str = os.getenv("IMAP_RECIEVER")
    VALIDATED_EMAIL: str = os.getenv("VERIFIED_EMAIL")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/test_db")