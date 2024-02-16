from src.env.globals import Global
from src.report.partlets.typing.scribe import PDFArtist

from abc import ABC
from typing import Callable

class Partlet(ABC):

	# Initialize shared empyt dict of strs ans functions
	_elements: dict[str, Callable] = {}

	# Created a variable to represent the height used in the PDF
	_height: int = 800

	draw = PDFArtist()

	def __init__(self):

		self.global_instance = Global()

		self.canvas = self.global_instance.get_canvas()

		self.calendar = self.global_instance.get_calendar()

		self.exec_date = self.global_instance.get_date()

	@classmethod
	def add_name_section(cls, section_name: str):
		"""
		Abstract method to add a name to the partlet.

		Args:
			section_name (str): The name of the section.
		"""
		null_lambda = lambda: None
		cls._elements[f"Starting the execution of section: {section_name}"] = null_lambda

	@classmethod
	def add_custom_element(cls, comment: str, function: Callable):
		"""
		Adds a custom function to the partlet.

		Args:
			comment (str): A comment describing the function.
			function (Callable): The function to add.
		"""
		cls._elements[comment] = function

	@classmethod
	def add_chapter_header(cls, text: str):
		"""
		Adds a chapter header to the partlet.

		Args:
			text (str): The text of the chapter header.
		"""
		chapter_header = lambda: cls.draw.centered_text(text=text, pattern="CHAPTER_HEADER", height=cls._height)
		cls._elements[f"Add a Header for the Chapter '{text}'"] = chapter_header

	@classmethod
	def add_title(cls, text: str):
		"""
		Adds a title to the partlet.

		Args:
			text (str): The text of the title.
		"""
		title = lambda: cls.draw.centered_text(text=text, pattern="TITLE", height=cls._height)
		cls._elements[f"Add a title"] = title

	@classmethod
	def add_subtitle(cls, text: str):
		"""
		Adds a subtitle to the partlet.

		Args:
			text (str): The text of the subtitle.
		"""
		sub_title = lambda: cls.draw.centered_text(text=text, pattern="SUBTITLE", height=cls._height)
		cls._elements[f"Add a formal subtitle"] = sub_title

	@classmethod
	def add_line(cls):
		"""
		Adds a horizontal line to the partlet.
		"""
		h_line = lambda: cls.draw.horizontal_line(cls._height)
		cls._elements["Add a Horizontal Line"] = h_line

	@classmethod
	def sub_height(cls, value: int):
		"""
		Subtracts a specified value from the height instance variable.
		
		Args:
			value (int): The value to subtract from the height.
		"""
		height_deduction = lambda: setattr(cls, '_height', cls._height - value)
		cls._elements[f"Reducing {value} from Height"] = height_deduction

	@classmethod
	def add_page(cls):
		"""
		Adds a new page to the report and reset height.
		"""
		skipper = lambda: cls.draw.blank_page()
		reset = lambda: setattr(cls, "_height", 800)
		cls._elements[f"Add a new page"] = skipper, reset

	@classmethod
	def exe_daily(cls):
		"""
		Executes the functions within the partlet for daily reporting.
		"""
		#print(cls._elements.keys())
		for key, function in cls._elements.items():
			print(f"Executing a function that: {key} | Height: {cls._height}")
			function()
