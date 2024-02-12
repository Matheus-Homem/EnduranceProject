from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from libs.utils.scribe import PDFArtist

class Singleton:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		# Setting initial height
		self.height = 800

	def subtract_height(self, value):
		self.height -= value

	def reset_height(self):
		self.height = 800

	def update(self, config):
		self.config = config

		# Create file path using get_partition_file function
		self.file_path = self.config.get_partitioned_file_path(f"{self.config.dt.dt}.pdf")

		# Instanciating canvas object
		self.canvas = Canvas(self.file_path, pagesize=A4)

		self.draw = PDFArtist(self.config)