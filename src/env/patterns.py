from src.env.helpers import Paths, PathsA
from src.env.globals import Global

from abc import ABC, abstractmethod
import logging
import os

class Process(ABC):
	
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	logger_path = Global().get_calendar().get_partitioned_file_path(prefix="LOG", fmt="txt")
	if os.path.exists(logger_path):
		os.remove(logger_path)
	handler = logging.FileHandler(logger_path)
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.INFO)
	logger.addHandler(console_handler)

	def __init__(self, paths:Paths):
		self.paths = paths
		self.globals = Global()
		self.calendar = self.globals.get_calendar()
		self.logger = self.get_logger()

	@abstractmethod
	def execute(self):
		pass

	def get_logger(self):
		return Process.logger
	
Process(paths=PathsA())