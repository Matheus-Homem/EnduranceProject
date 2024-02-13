from src.env.environment import EnvironmentConfig
from src.etl.cleaning_engine import DataCleaner
from src.etl.refining_engine import DataRefiner
import polars as pl
import time

class Orchestrator:
	
	def __init__(self, date_param):
		self.config = EnvironmentConfig(date_param=date_param)

	def execute_etl(self):
		print("ETL engine started.")
		# Perform data cleaning from raw to cleaned layer
		DataCleaner(self.config).execute()
		# Perform data refinement from cleaned to refined layer
		DataRefiner(self.config).execute()
		print("ETL engine finished.")

	def validate_last_date(self, file_path):
		print(f"Validating {file_path}")
		df_raw = pl.read_excel(self.config.get_file_path("ingestion", file_path))
		return self.config.dt.ingestion == df_raw.select(df_raw.columns[2])[-1]

	def block(self):
		# Check if dataframes are updated for automatic processes
		if self.validate_last_date("morning_routine_v2.xlsx") and self.validate_last_date("night_routine_v2.xlsx"):
			print("Pipeline Unblocked")
			return False  # Don't block the pipeline
		else:
			print("Pipeline Blocked")
			return True  # Block the pipeline

	def run_pipeline(self, automated: bool = False):
		if automated:
			# If process is automated, checks if both dataframes are updated
			print("Automation detected. Initializing validation.")
			while self.block():
				# Keep attempting pipeline execution while data validation blocks it
				print("Databases not updated. Retesting in 1 minute.")
				time.sleep(60)
			print("Validation finished.")
			self.execute_etl()
		else:
			# If process is manual, don't check if both dataframes are updated
			print("Manual process detected. Skipping validation.")
			# Execute the ETL process
			self.execute_etl()