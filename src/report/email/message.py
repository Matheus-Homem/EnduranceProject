from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os


class MessageBuilder:

    @staticmethod
    def create_multipart_message():
        return MIMEMultipart()

    @staticmethod
    def attach_subject(message, subject):
        message["Subject"] = subject
        return message

    @staticmethod
    def attach_text(message, text, text_type="plain"):
        message.attach(MIMEText(text, text_type))
        return message

    @staticmethod
    def attach_file(message, attachment_path):
        with open(attachment_path, "rb") as file:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(file.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", f"attachment; filename={os.path.split(attachment_path)[-1]}")
            message.attach(attachment)
        return message
