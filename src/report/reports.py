from src.env.helpers import Calendar
from src.report.email.manager import EmailManager



#from src.env.environment import EnvironmentConfig
from src.report.topics.header import Header
from src.report.topics.weight import WeightDiary
from src.report.topics import instance

from src.report.topics.partlet import *
from typing import List

class Report:
	
	def __init__(self, date_param):
		# Create a config class attribute from _config_instance
		self._config = EnvironmentConfig(date_param=date_param)
		
		# Create a sections attribute to list all Partlets inside Report
		self._sections: List[Partlet] = []

		self.calendar = Calendar(date_param)

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

	def send(self):
		email_manager = EmailManager()
		email_manager.set_frequency("0 5 * * *")
		email_manager.set_calendar(self.calendar)
		email_manager.dispatch()

	def daily_publish(self, send_email:bool=False):

		active_partlets = [Header(), WeightDiary()]
		[self.add_partlet(partlets) for partlets in active_partlets]

		## Report Saving
		self.save_file()

		if send_email:
			## Report Sending
			self.send_file()