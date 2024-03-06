from src.env.helpers import Paths
from src.env.globals import Global
from src.env.credentials import credentials

from abc import ABC, abstractmethod
import polars as pl
import logging
import os

class Orchestrator(ABC):
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


	def __init__(self):
		self.paths = Paths()

	@abstractmethod
	def execute(self):
		pass

	def validate_ingestion(self, 
			ingestion_path,
			cleaned_path,
			ingestion_dt_col="INFO1",
			cleaned_dt_col="day_date"
		):
		
		df_raw		= pl.read_json(ingestion_path)
		df_stored	= pl.read_parquet(cleaned_path)
		
		df_raw = df_raw.with_columns(casted_date_col=pl.col(ingestion_dt_col).cast(pl.Date))
		ingestion_date = df_raw["casted_date_col"]

		stored_dates = df_stored[cleaned_dt_col].unique()
		date_already_stored = stored_dates.is_in(ingestion_date).any()

		return date_already_stored

	def reading(self, file_format, file_path):
		self.logger.info(f"{self.process} Engine: READING Process Started")
		if file_format == "xlsx":
			df = pl.read_excel(file_path)
		elif file_format == "parquet":
			df = pl.read_parquet(file_path)
		elif file_format == "json":
			df = pl.read_json(file_path)
		self.logger.info(f"{self.process} Engine: READING Process Finished")
		return df
	
	def writing(self, df_to_write, file_path):
		self.logger.info(f"{self.process} Engine: WRITING Process Started")
		df_to_write.write_parquet(file_path)
		self.logger.info(f"{self.process} Engine: WRITING Process Finished")
	
	def validate_last_date(self, file_path):
		self.logger.info(f"Validating {file_path}")
		df = pl.read_excel(self.paths.get_file_path("ingestion", file_path))
		return self.paths.dt.ingestion == df.select(df.columns[2])[-1]