from libs.partlets import Partlet

class Report:
	def __init__(self, configuration, canvas):
		self.config = configuration
		self.c = canvas
		self.sections = []

	def add_partlet(self, partlet: Partlet):
		self.sections.append(partlet)

	def skip_page(self):
		pass

	def save(self, report_type):
		if report_type == "daily":
			for partlet in self.sections:
				partlet.daily_generate()
		elif report_type == "weekly":
			pass
		elif report_type == "monthly":
			pass
		
		self.c.save()

	def send(self):
		pass