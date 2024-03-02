from src.etl.patterns.orchestrator import Orchestrator
from src.etl.extracting.orchestrator import ExtractorOrchestrator
from src.etl.cleaning.orchestrator import CleanerOrchestrator
from src.etl.refining.orchestrator import RefinerOrchestrator

import time

class ProcessOrchestrator(Orchestrator):

	def orchestrate_process(self):
		self.logger.info("")
		self.logger.info("*********************************************************")
		self.logger.info(">>>>>>>>>>>>>>>> ETL PROCESS STARTED <<<<<<<<<<<<<<<<<<<<")
		self.logger.info("*********************************************************")
		self.logger.info("|----| EXTRACTING DATA: SOURCE -> INGESTION LAYER |-----|")
		ExtractorOrchestrator().execute()
		self.logger.info("*********************************************************")
		self.logger.info("|--| CLEANING DATA: INGESTION LAYER -> CLEANED LAYER |--|")
		CleanerOrchestrator().execute()
		self.logger.info("*********************************************************")
		self.logger.info("|---| REFINING DATA: CLEANED LAYER -> REFINED LAYER |---|")
		RefinerOrchestrator().execute()
		self.logger.info("*********************************************************")
		self.logger.info(">>>>>>>>>>>>>>>> ETL PROCESS FINISHED <<<<<<<<<<<<<<<<<<<<")
		self.logger.info("*********************************************************")

	def _block_pipeline(self):
		if self.validate_last_date("morning_routine_v2.xlsx") and self.validate_last_date("night_routine_v2.xlsx"):
			self.logger.info("Pipeline Unblocked")
			return False
		else:
			self.logger.info("Pipeline Blocked")
			return True 

	def execute(self, automated: bool = False):
		self.logger = Orchestrator.logger
		if automated:
			pass
			#self.logger.info("Automation detected. Initializing validation.")
			#while self._block_pipeline():
			#	self.logger.info("Databases not updated. Retesting in 1 minute.")
			#	time.sleep(60)
			#self.logger.info("Validation finished.")
			self.orchestrate_process()
		else:
			self.logger.info("Manual process detected. Skipping validation.")
			self.orchestrate_process()