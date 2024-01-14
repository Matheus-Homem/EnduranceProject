import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(config, subject="Assunto", email_body="Corpo", attachment_path=None):
	# Setting attachment_path to configuration.paths.filePdf if no value is provided
	attachment_path = attachment_path if attachment_path else config.get_file("report", f"{config.today.date}.pdf")
	
	# Build the message
	message = MIMEMultipart()
	message["From"] = config.smtp.username
	message["To"] = config.smtp.recipient
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
	with smtplib.SMTP(config.smtp.server, config.smtp.port) as server:
		server.starttls()
		server.login(config.smtp.username, config.smtp.password)
		server.sendmail(config.smtp.username, config.smtp.recipient, message.as_string())

	print("Email sent successfully!")
