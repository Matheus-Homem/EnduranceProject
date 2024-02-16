#import src.env.globals as glb
from src.report.partlets.partlet import Partlet
from src.report.partlets.engines.weight_engine import exec

from reportlab.lib.units import inch

class WeightPartlet(Partlet):
	def __init__(self):
		super().__init__()

		exec()
		#self.add_plot()
		Partlet.add_name_section(section_name="WEIGHT")
		Partlet.add_chapter_header("Pesagem")
		Partlet.sub_height(20)
		Partlet.add_line()
		Partlet.sub_height(20)	

	def add_plot(self):
		# Add a png plot to the PDF
		plot1_path = self.calendar.get_partitioned_file_path(prefix="WM", fmt="png")
		weight_plot = lambda: self.canvas.drawImage(plot1_path, inch, inch/4, width=6*inch, height=9.5*inch)
		weight_comment = "Add multiple Weight plots"
		Partlet.add_custom_element(comment=weight_comment, function=weight_plot)