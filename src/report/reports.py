import src.report.partlets as ptt
from src.env.globals import Global
from src.report.email.manager import EmailManager

from typing import List

class Report:

	def __init__(self):
		
		# Create a sections attribute to list all Partlets inside Report
		self._sections: List[ptt.Partlet] = []

		# Obter instâncias únicas de Calendar e Canvas
		self.canvas = Global().get_canvas()

	def add_partlet(self, partlet):
		self._sections.append(partlet)

	def save_file(self):
		for partlet in self._sections:
			partlet.exe_daily()
		self.canvas.save()
		print("PDF was successfully saved.")

	def send_file(self):
		email_manager = EmailManager()
		email_manager.set_frequency("0 5 * * *")
		email_manager.dispatch()

	def daily_publish(self, send_email:bool=False):

		active_partlets = [
			ptt.Header(), 
			ptt.WeightPartlet()
		]
		[self.add_partlet(partlets) for partlets in active_partlets]

		## Report Saving
		self.save_file()

		if send_email:
			## Report Sending
			self.send_file()

			