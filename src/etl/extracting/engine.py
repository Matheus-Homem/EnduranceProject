
from src.etl.patterns.engine import Engine
from src.etl.extracting.connection import IMAPConnection

import email
import json
import hashlib
import time


class ExtractorEngine(Engine):

	def __init__(self):
		super().__init__()


	def _build_connection(self):
		connection	= IMAPConnection()
		mail		= connection.get_mail()
		email_data	= connection.get_data()
		return mail, email_data

	def _generate_unique_filename(self, email_subject):
		form_id, email_date, email_timestamp = email_subject.split("_")
		form_id = form_id.split("-")[0]
		hash_obj = hashlib.sha256(email_timestamp.encode('utf-8'))
		hash_hex = hash_obj.hexdigest()
		unique_id = hash_hex[:8]
		return f"{form_id}_{email_date}({unique_id})"

	def _fetch_raw_email_content(self, num, mail):
		result, email_data = mail.fetch(num, '(RFC822)')
		return email_data[0][1]

	def _parse_email_message(self, raw_email):
		return email.message_from_bytes(raw_email)

	def _parse_email_body_content(self, msg):
		email_content_dict = {}

		body = (msg.get_payload(decode=True)
		  		   .decode('utf-8', 'ignore')
				   .replace("\r", "")
				   .replace("\n", " ")
			)
		
		for item in body.split("#")[1:]:
			question, response = item.split("|")
			email_content_dict[question] = response.strip()
		return email_content_dict

	def _get_json_path(self, msg):
		json_file_name = self._generate_unique_filename(msg['Subject'])
		return self.paths.get_file_path("ingestion", f"{json_file_name}.json")

	def _write_json_file(self, email_content_dict, json_path):
		with open(json_path, "w", encoding="utf-8") as arquivo:
			json.dump(email_content_dict, arquivo, indent=4, ensure_ascii=False)
	
	def _close_mail_connection(self, mail):
		mail.close()
		mail.logout()

	def _check_email_dates(self, num, mail):
		raw_email = self._fetch_raw_email_content(num, mail)
		msg = self._parse_email_message(raw_email)
		subject = msg['Subject']
		form_id, email_date, email_timestamp = subject.split("_")
		return email_date

	def _run_pipeline(self):
		mail, email_data = self._build_connection()
		for num in email_data[0].split():
			raw_email = self._fetch_raw_email_content(num, mail)
			msg = self._parse_email_message(raw_email)
			email_content_dict = self._parse_email_body_content(msg)
			json_path = self._get_json_path(msg)
			self._write_json_file(email_content_dict, json_path)
		self._close_mail_connection(mail)

	def _validate_pipeline(self, date_to_validate):
		mail, email_data = self._build_connection()
		for num in email_data[0].split():
			email_date = self._check_email_dates(num, mail)
			if email_date == date_to_validate:
				self.need_validation = False
			else: 
				pass
		self._close_mail_connection(mail)

	def execute(self, automated:bool):
		self.need_validation = automated
		date_to_validate = self.calendar.date_id

		if self.need_validation:
			while self.need_validation:
				self.logger.info(" |-----| VALIDATION STATUS: Validation Started |------| ")
				self._validate_pipeline(date_to_validate)
				if self.need_validation:
					time.sleep(60)					
				else:
					self.logger.info(" |-----| VALIDATION STATUS: Validation Finished |-----| ")
					self._run_pipeline()
		else:
			self.logger.info(" |------| VALIDATION STATUS: Validation Skipped |-----| ")
			self._run_pipeline()