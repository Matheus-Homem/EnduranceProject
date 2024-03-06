from src.etl.cleaning.formatter import Formatter

import polars as pl

class ExpressionsGenerator:

	def __init__(self, cleaning_schema):
		self.cleaning_schema = cleaning_schema

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

		self.formatter_function = {
			"date": Formatter.cast_to_date,
			"timedelta": Formatter.cast_to_timedelta,
			"timestamp": Formatter.cast_to_timedelta,
			"bool": Formatter.cast_to_boolean,
			"alias": Formatter.rename,
			"concatenate_two": Formatter.concatenate_two,
			"concatenate_four": Formatter.concatenate_four,
		}

	# def rename_expressions(self, identifier, columns_list):
	# 	column_dict = {index: column for index, column in enumerate(columns_list)}
	# 	return [
	# 		pl.col(column_dict[int(column_id)]).alias(column_config["rename_to"])
	# 		for column_id, column_config in self.cleaning_schema[identifier].items()
	# 	]
		
	def rename_expressions(self, identifier):
		rename_expressions = []

		for col_name, config in self.cleaning_schema.get(identifier).items():
			rename_function = self.formatter_function.get(config["method"])
			rename_expressions.append(rename_function(old_name=col_name, config=config))
		return rename_expressions

	def init_dtype_expressions(self, identifier):
		dtype_expressions = []

		for column_id, column_config in self.cleaning_schema[identifier].items():
			conversion_function = self.formatter_function.get(column_config["dtype"])
			if conversion_function:
				expression = (
					pl.col(column_config["rename_to"])
					.map_elements(conversion_function)
					.cast(self.dtype_dict[column_config["dtype"]])
					.alias(column_config["rename_to"])
				)
				dtype_expressions.append(expression)

		return dtype_expressions
	
	def final_dtype_expressions(self, identifier):
		dtype_expressions = []
		
		for column_id, column_config in self.cleaning_schema[identifier].items():
			if column_config["dtype"] == "timestamp":
				expression = Formatter.cast_to_timestamp(config=column_config)
			else:
				expression = pl.col(column_config["rename_to"])
			
			dtype_expressions.append(
				expression.cast(self.dtype_dict[column_config["dtype"]])
						  .alias(column_config["rename_to"]))
		
		return dtype_expressions