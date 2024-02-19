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
			for column_id, column_config in self.data_schema[table_id].items():
				return pl.col(column_id).alias(column_config["name"])
		elif table_id == "morning_v3":
			full_name_dict = {coluna[:3]+coluna[-4:]: coluna for coluna in columns_list}
			for column_id, column_config in self.data_schema[table_id].items():
				return pl.col(full_name_dict.get(column_id[:3])).alias(column_config["name"])

	def generate_dtype_expressions(self, table_id):
		for column_id, column_config in self.data_schema[table_id].items():
			return pl.col(column_config["name"]).cast(self.dtype_dict[column_config["dtype"]])