from src.etl.patterns.orchestrator import Orchestrator
from src.etl.cleaning.engine import CleanerEngine

import yaml
import polars as pl
from datetime import datetime

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

		## Cleaned Paths
		self.clnd_mrn_cold_path	= self.paths.get_file_path("cleaned",   "mrn_cleaned_cold.parquet")
		self.clnd_mrn_hot_path	= self.paths.get_file_path("cleaned",   "mrn_cleaned_hot.parquet")
		self.clnd_night_path	= self.paths.get_file_path("cleaned",   "ngt_cleaned.parquet")

		with open(self.yaml_path, 'r', encoding='utf-8') as file:
			self.data_schema = yaml.safe_load(file)

		self.engine = CleanerEngine(self.data_schema)

		# Relation of objects variable to manage the table_id, raw_path and cleaning_path
		self.tables_relation = [
			["morning_v2", self.raw_sun_path_v2, self.clnd_mrn_cold_path],
			["morning_v3", self.raw_sun_path_v3, self.clnd_mrn_hot_path],
			#["night",   self.raw_moon_path_v2,   self.clnd_night_path]
		]



	def cleaning(self, df_raw, table_id):

		self.logger.info(f"{self.process} Engine: EXECUTION Started")
		df_cleaned = self.engine.execute(df_to_execute=df_raw, table_id=table_id)
		self.logger.info(f"{self.process} Engine: EXECUTION Finished")
		return df_cleaned
	
		# Generate expressions
		df_raw3 = df_raw2.with_columns(
			pl.col("day_date").map_elements(lambda x: datetime.strptime(x, "%m-%d-%y").strftime("%Y-%m-%d")).alias("day_date")
		)
		df_raw4 = df_raw3.with_columns([
			(pl.col('day_form_time').map_elements(self._convert_time_to_microseconds)).alias('day_form_time'),
			(pl.col('slp_fall').map_elements(self._convert_time_to_microseconds)).alias('slp_fall'),
			(pl.col('pho_time').map_elements(self._convert_time_to_microseconds)).alias('pho_time'),
			(pl.col('slp_raise').map_elements(self._convert_time_to_microseconds)).alias('slp_raise'),
			(pl.col('slp_duration').map_elements(self._convert_time_to_microseconds)).alias('slp_duration')
		])
		df_raw5 = df_raw4.select(self.dtype_expression).sort("day_date")
		df_raw6 = df_raw5.with_columns([
			(pl.col("day_date").cast(pl.Datetime) + pl.duration(days=1, hours=pl.col("day_form_time").dt.hour(), minutes=pl.col("day_form_time").dt.minute())).alias("day_form_time"),
			(pl.col("day_date").cast(pl.Datetime) + pl.duration(days=0, hours=pl.col("slp_fall").dt.hour(),		 minutes=pl.col("slp_fall").dt.minute())).alias("slp_fall"),
			(pl.col("day_date").cast(pl.Datetime) + pl.duration(days=1, hours=pl.col("slp_raise").dt.hour(),	 minutes=pl.col("slp_raise").dt.minute())).alias("slp_raise")
		])
		df_cleaned = df_raw6.select(self.data_schema["columns"])

		print("Cleaning Engine: Cleaning Process Finished")

		return df_cleaned

	
	# Function to execute all the code combined
	def execute(self):
		# Gets the correct relation list from the tables_relation list
		for table_id, raw_path, cleaned_path in self.tables_relation:
			print("\n")
			print(f"Starting Cleaning Engine for {table_id}:")
			# Write the validated dataframe in the cleaned_path
			self.writing(
				# Validate the cleaned dataframe to contain only the correct user answers
				self.validating(
					# Cleans the correct raw dataframe with the use of table_id
					self.cleaning(
						# Read the chosen dataframe from the path given
						self.reading(
							file_format="xlsx",
							file_path=raw_path
						),
						table_id=table_id
					)
				),
				file_path=cleaned_path
			)