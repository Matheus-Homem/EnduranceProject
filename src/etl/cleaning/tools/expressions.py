import polars as pl

class Expressions:

	def __init__(
		self, 
		data_schema:dict,
		):
	
		self.data_schema = data_schema

		# Dict to translate dtype in STRING to dtype in POLARS
		self.dtype_dict = {
			"list": pl.List(pl.Utf8),
			"string": pl.Utf8,
			"date": pl.Date,
			"float": pl.Float64,
			"int": pl.Int64,
			"timestamp": pl.Datetime,
			"timedelta": pl.Duration
		}

	def generate_rename_expressions(self, table_id, columns_list):
		if table_id == "morning_v2":
			return [
				pl.col(column_id).alias(column_config["name"])
				for column_id, column_config in self.data_schema[table_id].items()	
			]
		elif table_id == "morning_v3":
			column_dict = {index: column for index, column in enumerate(columns_list)}
			return [
				pl.col(column_dict[int(column_id)]).alias(column_config["name"])
				for column_id, column_config in self.data_schema[table_id].items()				
			]
			
	def generate_dtype_expressions(self, table_id):
		return [
			pl.col(column_config["name"]).cast(self.dtype_dict[column_config["dtype"]])
			for column_id, column_config in self.data_schema[table_id].items()
		]