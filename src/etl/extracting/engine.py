
from src.etl.patterns.engine import Engine
from src.etl.extracting.connection import IMAPConnection

import email
import json
import hashlib
import time


class ExtractorEngine(Engine):

	def __init__(self):
		super().__init__()

		self.connection = IMAPConnection()
		self.mail = self.connection.get_mail()
		self.data = self.connection.get_data()


	def _generate_unique_filename(self, email_subject):
		form_id, email_date, email_timestamp = email_subject.split("_")
		form_id = form_id.split("-")[0]
		hash_obj = hashlib.sha256(email_timestamp.encode('utf-8'))
		hash_hex = hash_obj.hexdigest()
		unique_id = hash_hex[:8]
		return f"{form_id}_{email_date}({unique_id})"

	def _fetch_raw_email_content(self, num):
		result, email_data = self.mail.fetch(num, '(RFC822)')
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
	
	def _close_mail_connection(self):
		self.mail.close()
		self.mail.logout()

	def _check_email_dates(self, num):
		raw_email = self._fetch_raw_email_content(num)
		msg = self._parse_email_message(raw_email)
		subject = msg['Subject']
		form_id, email_date, email_timestamp = subject.split("_")
		return email_date

	def _build_json_message(self, num):
		raw_email = self._fetch_raw_email_content(num)
		msg = self._parse_email_message(raw_email)
		email_content_dict = self._parse_email_body_content(msg)
		json_path = self._get_json_path(msg)
		self._write_json_file(email_content_dict, json_path)

	def execute(self, automated:bool):
		need_validation = automated
		date_to_validate = self.calendar.date_id

		if need_validation:
			while need_validation:
				self.logger.info(" |---| VALIDATION STATUS: Validation Started |---| ")
				for num in self.data[0].split():
					email_date = self._check_email_dates(num)
					if email_date == date_to_validate:
						need_validation = False
					else: 
						pass
				if need_validation:
					self.logger.info(" |---| VALIDATION STATUS: Data Was Not Found |---| ")
					time.sleep(60)
				else:
					self.logger.info(" |-----| VALIDATION STATUS: Data Was Found |-----| ")
		else:
			self.logger.info(" |---| VALIDATION STATUS: Skipping Validation |--| ")
			for num in self.data[0].split():
				self._build_json_message(num)
			self._close_mail_connection()