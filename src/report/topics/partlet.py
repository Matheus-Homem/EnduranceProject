from src.report.topics import instance
from abc import ABC, abstractmethod
from typing import List, Callable


class Partlet(ABC):

	def __init__(self):
		# Initialize Partlet with a empyt list of elements
		self._elements: List[Callable] = []

		self.instance = instance
		self.draw = instance.draw
		self.config = instance.config
		self.draw.get_instance(instance)

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