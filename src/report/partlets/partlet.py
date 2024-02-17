from src.env.globals import Global
from src.report.partlets.typing.scribe import PDFArtist

import uuid
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
	def add_to_elements(
		cls, 
		description: str, 
		function: Callable
		):
		"""
		Adds an element to the _elements dictionary.

		Args:
			description (str): The description of the element.
			function (Callable): The lambda function to be added.
		"""
		unique_key = uuid.uuid4()
		cls._elements[f"{description}__{unique_key}"] = function

	@classmethod
	def add_name_section(
		cls, 
		section_name: str
		):
		"""
		Abstract method to add a name to the partlet.

		Args:
			section_name (str): The name of the section.
		"""
		cls.add_to_elements(
			description = f"Starting the execution of section: {section_name}", 
			function = lambda: None
		)

	@classmethod
	def add_custom_function(
		cls, 
		function_description: str, 
		custom_function: Callable
		):
		"""
		Adds a custom function to the partlet.

		Args:
			comment (str): A comment describing the function.
			custom_function (Callable): The function to add.
		"""
		cls.add_to_elements(
			description = function_description, 
			function = custom_function
		)

	@classmethod
	def add_chapter_header(
		cls, 
		chapter_name: str
		):
		"""
		Adds a chapter header to the partlet.

		Args:
			chapter_name (str): The text of the chapter header.
		"""
		cls.add_to_elements(
			description = f"Add a Header for the Chapter '{chapter_name}'", 
			function = lambda: cls.draw.centered_text(text=chapter_name, 
											 		  pattern="CHAPTER_HEADER", 
													  height=cls._height
													  )
		)

	@classmethod
	def add_title(
		cls, 
		title_text: str
		):
		"""
		Adds a title to the partlet.

		Args:
			title_text (str): The text of the title.
		"""
		cls.add_to_elements(
			description = "Add a title", 
			function = lambda: cls.draw.centered_text(text=title_text, 
													  pattern="TITLE", 
													  height=cls._height
													  )
		)

	@classmethod
	def add_subtitle(
		cls, 
		subtitle_text: str
		):
		"""
		Adds a subtitle to the partlet.

		Args:
			subtitle_text (str): The text of the subtitle.
		"""
		cls.add_to_elements(
			description = "Add a formal subtitle", 
			function = lambda: cls.draw.centered_text(text=subtitle_text, 
													  pattern="SUBTITLE", 
													  height=cls._height
													  )
		)

	@classmethod
	def add_line(
		cls
		):
		"""
		Add a horizontal line to the partlet.
		"""
		cls.add_to_elements(
			description = "Add a Horizontal Line", 
			function = lambda: cls.draw.horizontal_line(cls._height)
		)

	@classmethod
	def sub_height(
		cls, 
		value: int
		):
		"""
		Subtracts a specified value from the height instance variable.
		
		Args:
			value (int): The value to subtract from the height.
		"""
		cls.add_to_elements(
			description = f"Reducing {value} from Height",
			function = lambda: setattr(cls, '_height', cls._height - value)
		)

	@classmethod
	def add_page(
		cls
		):
		"""
		Adds a new page to the report and reset height.
		"""
		cls.add_to_elements(
			description = f"Skipping page",
			function = lambda: cls.draw.blank_page()
		)
		cls.add_to_elements(
			description = f"Reseting Height",
			function = lambda: setattr(cls, "_height", 800)
		)

	@classmethod
	def exe_daily(
		cls
		):
		"""
		Executes the functions within the partlet for daily reporting.
		"""
		for key, function in cls._elements.items():
			print(f"Height: {cls._height} || Executing : {key.split('__')[0]}")
			function()
