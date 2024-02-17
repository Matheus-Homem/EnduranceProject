from src.report.partlets.partlet import Partlet
from src.report.partlets.header.builder import Header
from src.report.partlets.weight.builder import WeightPartlet
from src.env.globals import Global
from src.report.email.manager import EmailManager

class Report:

	def __init__(self):

		self.canvas = Global().get_canvas()

	def _save_file(self):
		self.canvas.save()
		print("PDF was successfully saved.")

	def _send_file(self):
		email_manager = EmailManager()
		email_manager.set_frequency("0 5 * * *")
		email_manager.dispatch()

	def daily_publish(self, send_email:bool=False):
		Header()
		WeightPartlet()
		Partlet.exe_daily()

		## Report Saving
		self._save_file()

		if send_email:
			## Report Sending
			self._send_file()