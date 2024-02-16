from src.report.partlets.partlet import Partlet

class Header(Partlet):
	def __init__(self):
		super().__init__()

		self.subtitle_text = f"{self.calendar.dt_fmtd} | {self.draw.translate_weekday(self.calendar.week_day)} | Semana: {self.calendar.week_number}"
		
		Partlet.add_name_section(section_name="HEADER")
		Partlet.add_title("Relatório Diário")
		Partlet.sub_height(20)
		Partlet.add_subtitle(text=self.subtitle_text)
		Partlet.sub_height(10)
		Partlet.add_line()
		Partlet.sub_height(40)