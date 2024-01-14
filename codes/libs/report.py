class Report:
	def __init__(self, configuration, canvas):
		self.config = configuration
		self.c = canvas
		self.sections = []

	def add_partlet(self, partlet):
		partlet.generate_partlet()

	def skip_page(self):
		pass

	def save(self):
		
		
		self.c.save()

	def send(self):
		pass