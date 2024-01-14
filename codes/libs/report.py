from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class Report:
	def __init__(self, configuration):
		self.config = configuration

		# Create a canvas object to generate the PDF
		c = canvas.Canvas(
			self.config.get_file("report", f"{self.config.today.date}.pdf"), # File Name
			pagesize=A4
		)

		# Definition of the PDF page dimensions
		width, height = A4

	def add_section(self, section):
		self.section = section
		pass

	def skip_page():
		pass

	def save():
		pass

	def send():
		pass