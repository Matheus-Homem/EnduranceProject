from src.env.helpers import Paths
from src.env.credentials import Credentials
from src.env.globals import Global

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class EmailManager:
	def __init__(self):
		
		self.calendar = Global().get_calendar()
		self.message = MIMEMultipart()
		self.paths = Paths()

	def set_frequency(self, frequency):
		self.frequency = frequency
	
	def _build(self):
		print("Configuring e-mail")
		if self.frequency == "0 10 * * *":
			self.subject = f"Daily Report: {self.calendar.date}"
			self.email_body = f"""
				Daily Report
				Date: {self.calendar.dt_fmtd}
				Day of the Week: {self.calendar.week_day}
				Week Number: {self.calendar.week_number}
			"""

		self.message["From"] = Credentials.SMTP_USERNAME
		self.message["To"] = Credentials.SMTP_RECIPIENT
		self.message["Subject"] = self.subject

		self.message.attach(MIMEText(self.email_body, "plain"))

	def _attach(self):
		print("Attaching texts and files to e-mail")
		file_path = self.calendar.get_partitioned_file_path(fmt="pdf")
		self.attachment_path = file_path if file_path else None
		
		if self.attachment_path:
			with open(self.attachment_path, "rb") as file:
				attachment = MIMEBase("application", "octet-stream")
				attachment.set_payload(file.read())
				encoders.encode_base64(attachment)
				attachment.add_header("Content-Disposition", f"attachment; filename={os.path.split(self.attachment_path)[-1]}")
				self.message.attach(attachment)

	def _send(self):
		print("Sending e-mail")
		with smtplib.SMTP(Credentials.SMTP_SERVER, Credentials.SMTP_PORT) as server:
			server.starttls()
			server.login(Credentials.SMTP_USERNAME, Credentials.SMTP_PASSWORD)
			server.sendmail(
				from_addr=Credentials.SMTP_USERNAME, 
				to_addrs=Credentials.SMTP_RECIPIENT, 
				msg=self.message.as_bytes()
			)
		print("E-mail was send sucessfully")

	def dispatch(self):
		self._build()
		self._attach()
		self._send()
