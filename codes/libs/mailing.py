import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(self, subject:str, email_body:str, attachment_path:str):
	
	self.config, self.c, self.height = self.get_params()
	
	# Build the message
	message = MIMEMultipart()
	message["From"] = self.config.smtp.username
	message["To"] = self.config.smtp.recipient
	message["Subject"] = subject

	# Add the email body
	message.attach(MIMEText(email_body, "plain"))

	# Add attachment if provided
	if attachment_path:
		with open(attachment_path, "rb") as file:
			attachment = MIMEBase("application", "octet-stream")
			attachment.set_payload(file.read())
			encoders.encode_base64(attachment)
			attachment.add_header("Content-Disposition", f"attachment; filename={os.path.split(attachment_path)[-1]}")
			message.attach(attachment)

	# Connect to the SMTP server and send the email
	with smtplib.SMTP(self.config.smtp.server, self.config.smtp.port) as server:
		server.starttls()
		server.login(self.config.smtp.username, self.config.smtp.password)
		server.sendmail(self.config.smtp.username, self.config.smtp.recipient, message.as_string())

	print("Email sent successfully!")
