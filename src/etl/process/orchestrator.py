from src.etl.patterns.orchestrator import Orchestrator
from src.etl.cleaning.orchestrator import CleanerOrchestrator
from src.etl.refining.orchestrator import RefinerOrchestrator

import time

class ProcessOrchestrator(Orchestrator):

	def execute_etl(self):
		self.logger.info("")
		self.logger.info("ETL Process Started")
		self.logger.info("Performing data cleaning from ingestion layer to cleaned layer")
		CleanerOrchestrator().execute()
		self.logger.info("Performing data refining from cleaned layer to refining layer")
		RefinerOrchestrator().execute()
		self.logger.info("")
		self.logger.info("ETL Process Finished.")
		self.logger.info("")

	def _block_pipeline(self):
		if self.validate_last_date("morning_routine_v2.xlsx") and self.validate_last_date("night_routine_v2.xlsx"):
			self.logger.info("Pipeline Unblocked")
			return False
		else:
			self.logger.info("Pipeline Blocked")
			return True 

	def execute(self, automated: bool = False):
		if automated:
			self.logger.info("Automation detected. Initializing validation.")
			while self._block_pipeline():
				self.logger.info("Databases not updated. Retesting in 1 minute.")
				time.sleep(60)
			self.logger.info("Validation finished.")
			self.execute_etl()
		else:
			self.logger.info("Manual process detected. Skipping validation.")
			self.execute_etl()