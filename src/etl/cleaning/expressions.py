from src.etl.cleaning.formater import FormatConverter

import polars as pl

class ExpressionsGenerator:

	def __init__(self, data_schema):
		self.data_schema = data_schema

		self.dtype_dict = {
			"list": pl.List(pl.Utf8),
			"string": pl.Utf8,
			"date": pl.Date,
			"float": pl.Float64,
			"int": pl.Int64,
			"timestamp": pl.Datetime,
			"timedelta": pl.Duration,
			"bool": pl.Boolean
		}

		self.conversion_functions = {
			"date": FormatConverter._to_date,
			"timedelta": FormatConverter._to_timedelta,
			"timestamp": FormatConverter._to_timedelta,
			"bool": FormatConverter._to_boolean
		}

	def rename_expressions(self, identifier, columns_list):
		column_dict = {index: column for index, column in enumerate(columns_list)}
		return [
			pl.col(column_dict[int(column_id)]).alias(column_config["name"])
			for column_id, column_config in self.data_schema[identifier].items()
		]

	def init_dtype_expressions(self, identifier):
		dtype_expressions = []

		for column_id, column_config in self.data_schema[identifier].items():
			conversion_function = self.conversion_functions.get(column_config["dtype"])
			if conversion_function:
				expression = (
					pl.col(column_config["name"])
					.map_elements(conversion_function)
					.cast(self.dtype_dict[column_config["dtype"]])
					.alias(column_config["name"])
				)
				dtype_expressions.append(expression)

		return dtype_expressions
	
	def inal_dtype_expressions(self, identifier):
		dtype_expressions = []
		
		for column_id, column_config in self.data_schema[identifier].items():
			if column_config["dtype"] == "timestamp":
				expression = FormatConverter._to_timestamp(column_config=column_config)
			else:
				expression = pl.col(column_config["name"])
			
			dtype_expressions.append(
				expression.cast(self.dtype_dict[column_config["dtype"]])
						  .alias(column_config["name"]))
		
		return dtype_expressions