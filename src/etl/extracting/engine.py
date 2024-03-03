
from src.etl.patterns.engine import Engine
from src.etl.extracting.connection import IMAPConnection

import email
import json
import hashlib


class ExtractorEngine(Engine):

	def __init__(self):
		super().__init__()

		self.connection = IMAPConnection()
		self.mail = self.connection.get_mail()
		self.data = self.connection.get_data()

	def _generate_subject(self, email_subject):
		form_type, date_id, timestamp = email_subject.split("_")
		form_id = form_type.split("-")[0]
		hash_obj = hashlib.sha256(timestamp.encode('utf-8'))
		hash_hex = hash_obj.hexdigest()
		unique_id = hash_hex[:8]
		return f"{form_id}_{date_id}({unique_id})"

	def _fetch_raw_email(self, num):
		result, email_data = self.mail.fetch(num, '(RFC822)')
		return email_data[0][1]

	def _parse_email(self, raw_email):
		return email.message_from_bytes(raw_email)

	def _parse_email_body(self, msg):
		body = msg.get_payload(decode=True).decode('utf-8', 'ignore').replace("\r", "").replace("\n", " ")
		ask_dict = {}
		for item in body.split("#")[1:]:
			question, response = item.split("|")
			ask_dict[question] = response.strip()
		return ask_dict

	def _get_json_path(self, msg):
		subject = self._generate_subject(msg['Subject'])
		return self.paths.get_file_path("ingestion", f"{subject}.json")

	def _write_json_file(self, ask_dict, json_path):
		with open(json_path, "w", encoding="utf-8") as arquivo:
			json.dump(ask_dict, arquivo, indent=4, ensure_ascii=False)
	
	def _logout(self):
		self.mail.close()
		self.mail.logout()

	def execute(self):
		for num in self.data[0].split():
			raw_email = self._fetch_raw_email(num)
			msg = self._parse_email(raw_email)
			ask_dict = self._parse_email_body(msg)
			json_path = self._get_json_path(msg)
			self._write_json_file(ask_dict, json_path)
		self._logout()