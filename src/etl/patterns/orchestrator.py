from src.env.helpers import Paths
from src.env.globals import Global
from src.report.email.credentials import Credentials

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
		self.credentials = Credentials.from_env()

	@abstractmethod
	def execute(self):
		pass

	def reading(self, file_format, file_path):
		self.logger.info(f"{self.process} Engine: READING Process Started")
		if file_format == "xlsx":
			df = pl.read_excel(file_path)
		elif file_format == "parquet":
			df = pl.read_parquet(file_path)
		self.logger.info(f"{self.process} Engine: READING Process Finished")
		return df
	
	def writing(self, df_to_write, file_path):
		self.logger.info(f"{self.process} Engine: WRITING Process Started")
		df_to_write.write_parquet(file_path)
		self.logger.info(f"{self.process} Engine: WRITING Process Finished")

	def validating(self, df_to_validate):
		self.logger.info(f"{self.process} Engine: VALIDATING Process Started")
		df_validated = df_to_validate.filter(pl.col("email_confirmation") == self.credentials.get_verified_email())
		self.logger.info(f"{self.process} Engine: VALIDATING Process Finished")
		return df_validated
	
	def validate_last_date(self, file_path):
		self.logger.info(f"Validating {file_path}")
		df = pl.read_excel(self.paths.get_file_path("ingestion", file_path))
		return self.paths.dt.ingestion == df.select(df.columns[2])[-1]