from src.etl.patterns.orchestrator import Orchestrator
from src.etl.cleaning.engine import CleanerEngine

import yaml
import glob

class CleanerOrchestrator(Orchestrator):
	
	def __init__(self):
		super().__init__()
		
		self.process = "CLEANING"

		## Ingestion Path
		self.ingestion_paths_morning	= glob.glob(f"{self.paths.ingestion}/morning*.json")
		self.ingestion_paths_night		= glob.glob(f"{self.paths.ingestion}/night*.json")

		## Cleaned Paths
		self.cleaned_path_morning	= self.paths.get_file_path("cleaned", "morning.parquet")
		self.cleaned_path_night	= self.paths.get_file_path("cleaned", "ngt_cleaned.parquet")

		self.yaml_path = self.paths.get_file_path("yaml", "cleaning_config.yaml")

		with open(self.yaml_path, "r", encoding="utf-8") as file:
			self.cleaning_config = yaml.safe_load(file)

		self.engine = CleanerEngine(cleaning_schema=self.cleaning_config)

	def cleaning(self, df_raw, table_id):
		self.logger.info(f"{self.process} Engine: EXECUTION Started")
		df_cleaned = self.engine.execute(
			df_to_execute=df_raw,
			table_id=table_id,
			day_column="day_date"
		)
		self.logger.info(f"{self.process} Engine: EXECUTION Finished")
		return df_cleaned
	
	def execute(self):
		self.logger.info("*********************************************************")
		self.logger.info(f"////////////// STARTING CLEANING PROCESS ///////////////")
		self.logger.info("*********************************************************")

		# TODO= Create a loop for cleaning morning data and cleaning night data
		self.logger.info(f"//////////////// CLEANING MORNING DATA /////////////////")
		self.logger.info("*********************************************************")	
		for ingestion_path in self.ingestion_paths_morning:		
			
			ingestion_dt_is_stored = self.validate_ingestion(
				ingestion_path=ingestion_path, 
				cleaned_path=self.cleaned_path_morning
				)

			if ingestion_dt_is_stored:
				pass
			else:
				file_name = ingestion_path.split("ingestion")[1]
				processing_date = file_name[1:].split("_")[1].split("(")[0]
				self.logger.info(f" Date to be Cleaned: {processing_date} ")
				df_raw = self.reading(file_format="json", file_path=ingestion_path)
				df_stored = self.reading(file_format="parquet", file_path=self.cleaned_path_morning)
				
				df_cleaned = self.cleaning(df_raw=df_raw, table_id="morning")
				df_append = df_stored.vstack(df_cleaned)
				self.writing(df_to_write=df_append, file_path=self.cleaned_path_morning)
