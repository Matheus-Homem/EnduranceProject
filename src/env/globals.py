from src.env.helpers import Calendar

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

class Global:
	_instance = None

	def __new__(cls, exec_date=None):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
			cls._instance._exec_date = exec_date
			cls._instance._calendar = Calendar(exec_date)
			cls._instance._filename = cls._instance._calendar.get_partitioned_file_path(fmt="pdf")
			cls._instance._canvas = Canvas(filename=cls._instance._filename, pagesize=A4)
		return cls._instance

	def get_calendar(self):
		return self._calendar

	def get_canvas(self):
		return self._canvas
	
	def get_date(self):
		return self._exec_date
