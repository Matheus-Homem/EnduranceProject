from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from config.settings import Config
from libs.mailing import send_email
from libs.partlets import *
from typing import List

class Report:
	# Instanciate Config() class as _config_instance
	_config_instance = Config()
	
	def __init__(self):
		# Create a config class attribute from _config_instance
		self._config = self._config_instance
		
		# Create a sections attribute to list all Partlets inside Report
		self._sections: List[Partlet] = []

		self._height = 800

	def get_params(self) -> [Config(), Canvas(), int]:
		return self._config, self._c, self._height

	def add_partlet(self, partlet: Partlet):
		self._sections.append(partlet)

	def skip_page(self):
		pass

	def save_file(self):
		for partlet in self._sections:
			partlet.daily()

	def send_file(self):
		send_email(self,
				   subject = f"Daily Report: {self._config.dt.date}",
				   email_body = f"| Daily Report | Date: {self._config.dt.date_fmtd} | Day of the Week: {self._config.dt.week_day} | Week Number: {self._config.dt.week_number} |",
				   attachment_path = self._file_path
		)

	def daily_publish(self, date_str:str, send_email:bool=False):

		## 01. Configure Setttings	
		# Initiating DatesConfig classe with input date
		self._config.init_DatesConfig(date_str)

		# Create file path using get_partition_file function
		self._file_path = self._config.get_partitioned_file(f"{self._config.dt.date}.pdf")

		# Create a canvas object to generate the PDF
		self._c = Canvas(
			self._file_path,
			pagesize=A4
		)

		active_partlets = [Header(), WeightDiary()]
		[self.add_partlet(partlets) for partlets in active_partlets]

		## Report Saving
		self.save_file()

		if ~send_email:
			## Report Sending
			self.send_file()