from src.env.patterns import Process

import polars as pl


class Orchestrator(Process):


	def __init__(self):
		super().__init__()

	def validate_ingestion(self, 
			ingestion_path,
			cleaned_path,
			ingestion_dt_col="INFO1",
			cleaned_dt_col="day_date"
		):
		
		df_raw		= pl.read_json(ingestion_path)
		df_stored	= pl.read_parquet(cleaned_path)
		
		df_raw			= df_raw.with_columns(casted_date_col=pl.col(ingestion_dt_col).cast(pl.Date))
		ingestion_date	= df_raw["casted_date_col"]

		stored_dates		= df_stored[cleaned_dt_col].unique()
		date_already_stored	= stored_dates.is_in(ingestion_date).any()

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