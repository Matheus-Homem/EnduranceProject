from src.env.globals import Global
from src.env.helpers import Paths
import json

class PDFArtist:
	def __init__(self):
		self.paths = Paths()
		self.canvas = Global().get_canvas()
		self.load_json()

	def load_json(self):
		weekday_name_file_path = self.paths.get_file_path("json", "ptbr_weekday_name.json")
		with open(weekday_name_file_path, 'r', encoding="utf-8") as f:
			self.translate_ptbr = json.load(f)
			
		font_patterns_file_path = self.paths.get_file_path("json", "font_patterns.json")
		with open(font_patterns_file_path, 'r') as f:
			self.font_patterns = json.load(f)

	def centered_text(self, text, pattern, height):
		font, font_size = self.load_font(pattern)
		text_width = self.canvas.stringWidth(text, font, font_size)
		left_start = (595.276 - text_width) / 2
		self.canvas.setFont(font, font_size)
		self.canvas.drawString(left_start, height, text)

	def horizontal_line(self, height):
		self.canvas.line(100, height, 500, height)

	def blank_page(self):
		self.canvas.showPage()

	def load_font(self, font_type):
		font = self.font_patterns[font_type]["font"]
		font_size = self.font_patterns[font_type]["font_size"]
		return font, font_size

	def translate_weekday(self, english_weekday):
		return self.translate_ptbr[english_weekday]