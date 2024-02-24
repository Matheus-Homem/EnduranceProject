from src.etl.patterns.orchestrator import Orchestrator
from src.etl.cleaning.engine import CleanerEngine

import yaml

class CleanerOrchestrator(Orchestrator):
	
	def __init__(self):
		super().__init__()
		
		self.process = "CLEANING"

		## Raw Morning Paths
		self.raw_sun_path_v2	= self.paths.get_file_path("ingestion", "morning_routine_v2.xlsx")
		self.raw_sun_path_v3	= self.paths.get_file_path("ingestion", "morning_data_02_24.xlsx")
		
		## Raw Night Paths
		self.raw_moon_path_v2	= self.paths.get_file_path("ingestion", "night_routine_v2.xlsx")
		self.raw_moon_path_v3	= self.paths.get_file_path("ingestion", "night_data_02_24.xlsx")
		self.raw_moon_path_v4	= self.paths.get_file_path("ingestion", "night_compass_03_24.xlsx")

		## Cleaned Paths
		self.clnd_mrn_cold_path	= self.paths.get_file_path("cleaned",   "mrn_cleaned_cold.parquet")
		self.clnd_mrn_hot_path	= self.paths.get_file_path("cleaned",   "mrn_cleaned_hot.parquet")
		self.clnd_night_path	= self.paths.get_file_path("cleaned",   "ngt_cleaned.parquet")

		self.yaml_path = self.paths.get_file_path("yaml", "data_schema.yaml")

		with open(self.yaml_path, 'r', encoding='utf-8') as file:
			self.data_schema = yaml.safe_load(file)

		self.engine = CleanerEngine(self.data_schema)

		self.tables_relation = [
			["morning_v2", self.raw_sun_path_v2, self.clnd_mrn_cold_path, "morning"],
			["morning_v3", self.raw_sun_path_v3, self.clnd_mrn_hot_path, "morning"],
			["night_0324", self.raw_moon_path_v4, self.clnd_night_path, "night"]
		]

	def cleaning(self, df_raw, table_id, mrng_or_night):
		self.logger.info(f"{self.process} Engine: EXECUTION Started")
		df_cleaned = self.engine.execute(
			df_to_execute=df_raw,
			table_id=table_id,
			day_column="day_date",
			mrng_or_night=mrng_or_night
		)
		self.logger.info(f"{self.process} Engine: EXECUTION Finished")
		return df_cleaned
	
	def execute(self):
		self.logger = Orchestrator.logger
		for table_id, raw_path, cleaned_path, mrng_or_night in self.tables_relation:
			self.logger.info("*********************************************************")
			self.logger.info(f"///////// STARTING {table_id} CLEANING PROCESS /////////")
			self.logger.info("*********************************************************")

			raw_data = self.reading(file_format="xlsx", file_path=raw_path)
			
			cleaned_data = self.cleaning(df_raw=raw_data, table_id=table_id, mrng_or_night=mrng_or_night)

			validated_data = self.validating(df_to_validate=cleaned_data)

			self.writing(df_to_write=validated_data, file_path=cleaned_path)
