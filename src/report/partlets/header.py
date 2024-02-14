from src.report.partlets.partlet import Partlet

class Header(Partlet):
	def __init__(self):
		super().__init__()

		self.subtitle_text = f"{self.calendar.dt_fmtd} | {self.draw.translate_weekday(self.calendar.week_day)} | Semana: {self.calendar.week_number}"
		self.order_elements(section_name="HEADER")
		
	def order_elements(self, section_name: str):
		super().order_elements(section_name)
		self.add_title("Relatório Diário")
		self.sub_height(20)
		self.add_subtitle(self.subtitle_text)
		self.sub_height(10)
		self.add_line()
		self.sub_height(40)