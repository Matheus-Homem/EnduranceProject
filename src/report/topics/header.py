from src.report.topics.partlet import Partlet

class Header(Partlet):
	def __init__(self):
		super().__init__()

		self.set_order()

	def exe_title(self):
		# Title
		title = lambda: self.draw.centered_text(text="Relatório Diário", pattern="TITLE")
		self._elements.append(title)

	def exe_subtitle(self):
		# Subtitle with date, weekday, and week number
		subtitle_text = f"{self.config.dt.dt_fmtd} | {self.draw.translate_weekday(self.config.dt.week_day)} | Semana: {self.config.dt.week_number}"
		subtitle = lambda: self.draw.centered_text(text=subtitle_text, pattern="SUBTITLE")
		self._elements.append(subtitle)
		
	def set_order(self):
		self.exe_title() # Create a Title for the Header Partlet
		self.exe_subtraction(20) # Subtract 20 from initial height
		self.exe_subtitle() # Create a Subitle for the Header Partlet
		self.exe_subtraction(10) # Subtract 10 from initial height
		self.exe_line()  # Create a Horizontal Line for the Header Partlet
		self.exe_subtraction(40) # Subtract 40 from initial 