import src.report.partlets as ptt
from src.env.helpers import Calendar
from src.report.singletons import CanvasSingleton
from src.report.email.manager import EmailManager

from typing import List

class Report:

	def __init__(self, exec_date):
		
		# Create a sections attribute to list all Partlets inside Report
		self._sections: List[ptt.Partlet] = []

		self.calendar = Calendar(exec_date)

		self.file_path = self.calendar.get_partitioned_file_path(fmt="pdf")

		self.canvas = CanvasSingleton(filename=self.file_path).get_canvas()

	def add_partlet(self, partlet: ptt.Partlet):
		self._sections.append(partlet)

	def skip_page(self):
		pass

	def save_file(self):
		for partlet in self._sections:
			partlet.daily()
		self.canvas.save()

	def send(self):
		email_manager = EmailManager()
		email_manager.set_frequency("0 5 * * *")
		email_manager.set_calendar(self.calendar)
		email_manager.dispatch()

	def daily_publish(self, send_email:bool=False):

		active_partlets = [
			ptt.Header(), 
			ptt.WeightDiary()
		]
		[self.add_partlet(partlets) for partlets in active_partlets]

		## Report Saving
		self.save_file()

		if send_email:
			## Report Sending
			self.send_file()