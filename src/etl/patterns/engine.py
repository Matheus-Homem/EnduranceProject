from abc import ABC, abstractmethod
from src.env.helpers import Paths

class Engine(ABC):
	
	def __init__(self):
		self.paths = Paths()

	@abstractmethod
	def execute(self):
		pass