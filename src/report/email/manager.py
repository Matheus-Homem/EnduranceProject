from src.env.paths import Paths
from src.report.email.credentials import Credentials

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class EmailManager:
	def __init__(self):
		
		# Instanciate MIMEMultipart as message
		self.message = MIMEMultipart()

		# Instanciate Paths
		self.paths = Paths()

		# Instanciate Credentials
		self.credentials = Credentials.from_env()
		
		# Get all credentials variables
		self.get_credentials()

	def set_frequency(self, frequency):
		self.frequency = frequency

	def set_calendar(self, calendar_instance):
		self.calendar = calendar_instance

	def get_credentials(self):
		self.username = self.credentials.get_username()
		self.recipient = self.credentials.get_recipient()
		self.password = self.credentials.get_password()
		self.server = self.credentials.get_server()
		self.port = self.credentials.get_port()
	
	def build(self):
		if self.frequency == "0 5 * * *":
			self.subject = f"Daily Report: {self.calendar.date}",
			self.email_body = f"""
				Daily Report
				Date: {self.calendar.date_fmtd}
				Day of the Week: {self.calendar.week_day}
				Week Number: {self.calendar.week_number}
			"""
	
		# Build the message
		self.message["From"] = self.username
		self.message["To"] = self.recipient
		self.message["Subject"] = self.subject

		# Add the email body
		self.message.attach(MIMEText(self.email_body, "plain"))

	def attach(self):
		# Create file path using get_partition_file function
		file_path = self.paths.get_partitioned_file_path(f"{self.calendar.date}.pdf")
		self.attachment_path = file_path if file_path else None
		
		# Add attachment if provided
		if self.attachment_path:
			with open(self.attachment_path, "rb") as file:
				attachment = MIMEBase("application", "octet-stream")
				attachment.set_payload(file.read())
				encoders.encode_base64(attachment)
				attachment.add_header("Content-Disposition", f"attachment; filename={os.path.split(self.attachment_path)[-1]}")
				self.message.attach(attachment)

	def send(self):
		# Connect to the SMTP server and send the email
		with smtplib.SMTP(self.credentials.get_server(), self.credentials.get_port()) as server:
			server.starttls()
			server.login(self.credentials.username, self.credentials.password)
			server.sendmail(self.credentials.username, self.credentials.recipient, self.message.as_string())

	def dispatch(self):
		self.build()
		self.attach()
		self.send()
