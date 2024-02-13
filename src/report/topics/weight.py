from src.report.topics.partlet import Partlet
from reportlab.lib.units import inch

class WeightDiary(Partlet):
	def __init__(self):
		super().__init__()

		self.set_order()

	def exe_title(self):
		# Subtitle identifing Pesagem (Weighting)
		title = lambda: self.draw.centered_text(text="Pesagem", pattern="CHAPTER_HEADER")
		self._elements.append(title)

	def exe_plot(self):
		# Adicione uma imagem PNG ao PDF
		plot1_path = self.config.get_partitioned_file_path(f"WM_{self.config.dt.date}.png")
		plot = lambda: self.instance.canvas.drawImage(plot1_path, inch, inch/4, width=6*inch, height=9.5*inch)
		self._elements.append(plot)

	def set_order(self):
		self.exe_title() # Create a Title for the Weight Partlet
		self.exe_subtraction(20) # Subtract 20 from initial height
		self.exe_line() # Create a Horizontal Line for the Weight Partlet
		self.exe_subtraction(20) # Subtract 20 from initial height
		self.exe_plot() # Create a plot for Weight
		self.skip_page()