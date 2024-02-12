import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email(self, frequency):
	
	self.config  = self.get_report_config()

	# Create file path using get_partition_file function
	self._file_path = self.config.get_partitioned_file_path(f"{self.config.dt.dt}.pdf")

	if frequency == "0 5 * * *":
		self.subject = f"Daily Report: {self.config.dt.dt}",
		self.email_body = f"| Daily Report | Date: {self.config.dt.date_fmtd} | Day of the Week: {self.config.dt.week_day} | Week Number: {self.config.dt.week_number} |",
		self.attachment_path = self.file_path
	
	# Build the message
	message = MIMEMultipart()
	message["From"] = self.config.email.username
	message["To"] = self.config.email.recipient
	message["Subject"] = self.subject

	# Add the email body
	message.attach(MIMEText(self.email_body, "plain"))

	# Add attachment if provided
	if self.attachment_path:
		with open(self.attachment_path, "rb") as file:
			attachment = MIMEBase("application", "octet-stream")
			attachment.set_payload(file.read())
			encoders.encode_base64(attachment)
			attachment.add_header("Content-Disposition", f"attachment; filename={os.path.split(self.attachment_path)[-1]}")
			message.attach(attachment)

	# Connect to the SMTP server and send the email
	with smtplib.SMTP(self.config.email.server, self.config.email.port) as server:
		server.starttls()
		server.login(self.config.email.username, self.config.email.password)
		server.sendmail(self.config.email.username, self.config.email.recipient, message.as_string())

	print("Email sent successfully!")
