from reportlab.lib import fonts

class Font:
	def __init__(self, family='Helvetica', size=12, style='Normal'):
		self.family = family
		self.size = size
		self.style = style

	def set_family(self, family):
		self.family = family

	def set_size(self, size):
		self.size = size

	def set_style(self, style):
		self.style = style

	def get_reportlab_font(self):
		return fonts.Font(self.family, self.size, self.style)