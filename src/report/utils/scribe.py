import json

class PDFArtist:
	def __init__(self, config):
		self.config = config

		self.load_json()

	def load_json(self):
		weekday_name_file_path = self.config.get_file_path("json", "ptbr_weekday_name.json")
		with open(weekday_name_file_path, 'r', encoding="utf-8") as f:
			self.translate_ptbr = json.load(f)
			
		font_patterns_file_path = self.config.get_file_path("json", "font_patterns.json")
		with open(font_patterns_file_path, 'r') as f:
			self.font_patterns = json.load(f)

	def get_instance(self, instance):
		self.instance = instance

	def centered_text(self, text, pattern):
		font, font_size = self.load_font(pattern)
		text_width = self.instance.canvas.stringWidth(text, font, font_size)
		left_start = (595.276 - text_width) / 2
		self.instance.canvas.setFont(font, font_size)
		print("dentro da função:", self.instance.height)
		self.instance.canvas.drawString(left_start, self.instance.height, text)

	def horizontal_line(self):
		print("dentro da função:", self.instance.height)
		self.instance.canvas.line(100, self.instance.height, 500, self.instance.height)

	def load_font(self, font_type):
		font = self.font_patterns[font_type]["font"]
		font_size = self.font_patterns[font_type]["font_size"]
		return font, font_size

	def translate_weekday(self, english_weekday):
		return self.translate_ptbr[english_weekday]