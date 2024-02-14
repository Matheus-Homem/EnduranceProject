from src.env.globals import Global
from src.report.height import Height
from src.report.partlets.typing.scribe import PDFArtist

from abc import ABC, abstractmethod
from typing import Dict, Callable

class Partlet(ABC):

	def __init__(self):

		# Initialize Partlet with a empyt dict of strs ans functions
		self._elements: Dict[str, Callable] = {}

		#self.global_instance = Global()
		self.global_instance = Global()

		# Get canvas intance from globals
		self.canvas = self.global_instance.get_canvas()

		# Get exec_date value from globals
		self.exec_date = self.global_instance.get_date()

		# Get global calendar
		self.calendar = self.global_instance.get_calendar()

		# Intanciate Height class
		self.height_instance = Height()

		# Instanciate PDFArtist class
		self.draw = PDFArtist()

		# Get int height value from height instance
		self.height = self.height.get()

	@abstractmethod
	def order_elements(self, section_name:str):
		null_lambda = lambda: None
		self._elements[f"Starting the execution of section: {section_name}"] = null_lambda

	def add_custom_element(self, comment:str, function:Callable):
		# Adds a custom function
		self._elements[comment] = function

	def add_chapter_header(self, text:str):
		# Draw the Header of a Chapter
		chapter_header = lambda: self.draw.centered_text(text=text, pattern="CHAPTER_HEADER")
		self._elements[f"Add a Header for the Chapter '{text}'"] = chapter_header

	def add_title(self, text:str):
		# Draw a Title
		title = lambda: self.draw.centered_text(text=text, pattern="TITLE")
		self._elements[f"Add a title"] = title

	def add_subtitle(self, text:str):
		# Draw a formal Subtitle
		sub_title = lambda: self.draw.centered_text(text=text, pattern="SUBTITLE", height=self.height)
		self._elements[f"Add a formal subtitle"] = sub_title

	def add_line(self):
		# Draw horizontal line
		h_line = lambda: self.draw.horizontal_line(self.height)
		self._elements["Add a Horizontal Line"] = h_line

	def sub_height(self, value:int):
		# Subtract a value from height
		height_deduction = lambda: self.height_instance.subtract(value)
		self._elements[f"Subtract {value} from Height"] = height_deduction

	def add_page(self):
		skipper = lambda: self.canvas.showPage()
		self._elements[f"Add a new page"] = skipper

	def exe_daily(self):
		for key, function in self._elements.items():
			print(self.height_instance.get())
			print(f"Executing a function that: {key}")
			function()