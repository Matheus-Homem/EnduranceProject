from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

class CanvasSingleton:
    _instance = None
    _filename = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, filename=None):
        if filename and not self._filename:
            self._filename = filename
            self._canvas = Canvas(filename=filename, pagesize=A4)
        elif self._filename:
            self._canvas = Canvas(filename=self._filename, pagesize=A4)
        else:
            raise ValueError("You must specify a filename when creating the first instance of Canvas.")

    def get_canvas(self):
        return self._canvas

class Height:
	_instance = None

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls, *args, **kwargs)
		return cls._instance

	def __init__(self):
		self.reset()

	def reset(self):
		self._value = 800

	def subtract(self, value):
		self._value -= value

	def get(self):
		return self._value