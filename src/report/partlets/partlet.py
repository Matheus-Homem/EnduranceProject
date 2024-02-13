from src.report.singletons import Height, CanvasSingleton
from src.report.utils.scribe import PDFArtist

from abc import ABC, abstractmethod
from typing import List, Callable

class Partlet(ABC):

	def __init__(self):
		# Initialize Partlet with a empyt list of elements
		self._elements: List[Callable] = []

		self.height = Height()
		self.canvas = CanvasSingleton().get_canvas()
		self.draw = PDFArtist()

	def exe_line(self):
		# Draw horizontal line
		h_line = lambda: self.draw.horizontal_line()
		self._elements.append(h_line)

	def exe_subtraction(self, value):
		height_deduction = lambda: self.instance.subtract_height(value)
		self._elements.append(height_deduction)

	def skip_page(self):
		skipper = lambda: self.instance.canvas.showPage()
		self._elements.append(skipper)

	def daily(self):
		for func in self._elements:
			func()