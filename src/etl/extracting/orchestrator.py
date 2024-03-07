from src.etl.patterns.orchestrator import Orchestrator
from src.etl.extracting.engine import ExtractorEngine



class ExtractorOrchestrator(Orchestrator):
	
	def __init__(self):
		super().__init__()

		self.process = "EXTRACTING"

		self.engine = ExtractorEngine()

	def execute(self, automated:bool):
		self.logger.info("*********************************************************")
		self.logger.info(f"///////////// STARTING EXTRACTING PROCESS //////////////")
		self.logger.info("*********************************************************")
		self.engine.execute(automated=automated)

