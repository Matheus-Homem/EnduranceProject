from env.environment import EnvironmentConfig
from .topics.header import Header
from .topics.weight import WeightDiary
from .topics import instance

from libs.utils.mailing import send_email
from libs.topics.partlet import *
from typing import List

class Report:
	
	def __init__(self, date_param):
		# Create a config class attribute from _config_instance
		self._config = EnvironmentConfig(date_param=date_param)
		
		# Create a sections attribute to list all Partlets inside Report
		self._sections: List[Partlet] = []

		instance.update(self._config)

	def get_report_config(self):
		return self._config

	def add_partlet(self, partlet: Partlet):
		self._sections.append(partlet)

	def skip_page(self):
		pass

	def save_file(self):
		for partlet in self._sections:
			partlet.daily()
		instance.canvas.save()

	def send_file(self):
		send_email(self,
				   subject = f"Daily Report: {self._config.dt.dt}",
				   email_body = f"| Daily Report | Date: {self._config.dt.date_fmtd} | Day of the Week: {self._config.dt.week_day} | Week Number: {self._config.dt.week_number} |",
				   attachment_path = self._file_path
		)

	def daily_publish(self, send_email:bool=False):

		active_partlets = [Header(), WeightDiary()]
		[self.add_partlet(partlets) for partlets in active_partlets]

		## Report Saving
		self.save_file()

		if send_email:
			## Report Sending
			self.send_file()