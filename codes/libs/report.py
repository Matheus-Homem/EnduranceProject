class Report:
	def __init__(self, configuration, canvas):
		self.config = configuration
		self.c = canvas
		self.sections = []

	def add_partlet(self, partlet):
		self.sections.append(partlet)

	def skip_page(self):
		pass

	def save(self):
		for partlet in self.sections:
			partlet.generate_partlet()
		
		self.c.save()

	def send(self):
		pass