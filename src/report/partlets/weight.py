#import src.env.globals as glb
from src.report.partlets.partlet import Partlet
from src.report.partlets.engines.weight_engine import exec

from reportlab.lib.units import inch

class WeightPartlet(Partlet):
	def __init__(self):
		super().__init__()

		self.order_elements(section_name="WEIGHT")
		exec()

	def add_plot(self):
		# Add a png plot to the PDF
		plot1_path = self.calendar.get_partitioned_file_path(prefix="WM", fmt="png")
		weight_plot = lambda: self.canvas.drawImage(plot1_path, inch, inch/4, width=6*inch, height=9.5*inch)
		weight_comment = "Add multiple Weight plots"
		self.add_custom_element(comment=weight_comment, function=weight_plot)

	def order_elements(self, section_name: str):
		super().order_elements(section_name)
		self.add_chapter_header("Pesagem")
		self.sub_height(20)
		self.add_line()
		self.sub_height(20)
		self.add_plot()