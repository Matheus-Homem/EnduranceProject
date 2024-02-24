from abc import ABC, abstractmethod


class Engine(ABC):
	

	@abstractmethod
	def execute(self):
		pass