from src.etl.patterns.orchestrator import Orchestrator
from src.etl.extracting.orchestrator import ExtractorOrchestrator
from src.etl.cleaning.orchestrator import CleanerOrchestrator
from src.etl.refining.orchestrator import RefinerOrchestrator



class ProcessOrchestrator(Orchestrator):


	def execute(self, automated:bool):

		self.logger.info("*********************************************************")
		self.logger.info(">>>>>>>>>>>>>>>> ETL PROCESS STARTED <<<<<<<<<<<<<<<<<<<<")
		self.logger.info("*********************************************************")
		self.logger.info("|----| EXTRACTING DATA: SOURCE -> INGESTION LAYER |-----|")
		ExtractorOrchestrator().execute(automated=automated)
		self.logger.info("*********************************************************")
		self.logger.info("|--| CLEANING DATA: INGESTION LAYER -> CLEANED LAYER |--|")
		CleanerOrchestrator().execute()
		self.logger.info("*********************************************************")
		self.logger.info("|---| REFINING DATA: CLEANED LAYER -> REFINED LAYER |---|")
		RefinerOrchestrator().execute()
		self.logger.info("*********************************************************")
		self.logger.info(">>>>>>>>>>>>>>>> ETL PROCESS FINISHED <<<<<<<<<<<<<<<<<<<<")
		self.logger.info("*********************************************************")