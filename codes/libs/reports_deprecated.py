import json

from abc import ABC, abstractmethod

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors

class Report(ABC):
	
	def __init__(self, configuration):
		self.config = configuration
		self.report_date = configuration.today.date

		font_patterns_path = os.path.join(self.paths.misc_dir, 'font_patterns.json')
		with open(font_patterns_path, 'r') as f:
			self.font_patterns = json.load(f)

	@abstractmethod
	def canvas_config(self):
		pass

	@abstractmethod
	def add_header(self):
		pass

	@abstractmethod
	def generate_report(self):
		pass

	def centralize_text(self, canvas, initial_height, text, font_pattern):
		canvas.setFont(self.font_patterns[font_pattern]['font'], self.font_patterns[font_pattern]['font_size'])
		canvas.drawString(0, altura_inicial, texto)
		canvas.setFont(fonte, tamanho_fonte)
		largura_texto = canvas.stringWidth(texto, fonte, tamanho_fonte)
		posicao_inicial = (595.276 - largura_texto) / 2
		canvas.drawString(posicao_inicial, altura_inicial, texto)

class DailyReport(Report):
	
	def __init__(self, report_date):
		super().__init__(report_date)

	def canvas_config(self):
		pass
		
	def add_header(self):
		pass

	def generate_report(self):
		pass

class WeeklyReport(Report):
	pass

class MonthlyReport(Report):
	pass