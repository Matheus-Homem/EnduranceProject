import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(configuration, subject="Assunto", email_body="Corpo", attachment_path=None):
    # Setting attachment_path to configuration.paths.filePdf if no value is provided
	attachment_path = attachment_path if attachment_path else configuration.paths.report_file
	
	# Build the message
	message = MIMEMultipart()
	message["From"] = configuration.smtp.username
	message["To"] = configuration.smtp.recipient
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
	with smtplib.SMTP(configuration.smtp.server, configuration.smtp.port) as server:
		server.starttls()
		server.login(configuration.smtp.username, configuration.smtp.password)
		server.sendmail(configuration.smtp.username, configuration.smtp.recipient, message.as_string())

	print("Email sent successfully!")
