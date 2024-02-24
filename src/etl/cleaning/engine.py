from src.etl.patterns.engine import Engine

import polars as pl
from datetime import datetime




class CleanerEngine(Engine):

	def __init__(self, data_schema):

		self.data_schema = data_schema

		self.expressions = Expressions(data_schema=data_schema)

	def _convert_time_to_microseconds(self, time_str):
		if time_str:
			time_converted_to_time64 = datetime.strptime(time_str, "%H:%M")
			difference_from_midnight = time_converted_to_time64 - datetime.strptime("00:00", "%H:%M")
			total_microseconds = int(difference_from_midnight.total_seconds() * 1e6)
			return total_microseconds
		else:
			return None

	def execute(self, df_to_execute, table_id):
		
		self.rename_expression = self.expressions.generate_rename_expressions(table_id=table_id, columns_list=df_to_execute.columns)
		
		lista_de_expressoes = []
		lista_de_expressoes2 = []
		for column_id, column_config in self.data_schema["morning_v3"].items():
			if column_config["dtype"]=="date":
				expr = (
					pl.col(column_config["name"])
					.map_elements(lambda x: datetime.strptime(x, "%m-%d-%y").strftime("%Y-%m-%d"))
					.cast(self.dtype_dict[column_config["dtype"]])
					.alias(column_config["name"])
				)
				lista_de_expressoes.append(expr)
			elif column_config["dtype"] in ["timedelta", "timestamp"]:
				expr = (
					pl.col(column_config["name"])
					.map_elements(self._convert_time_to_microseconds)
					.cast(self.dtype_dict[column_config["dtype"]])
					.alias(column_config["name"])
				)
				lista_de_expressoes.append(expr)

		for column_id, column_config in self.data_schema["morning_v3"].items():
			if column_config["dtype"]=="timestamp":
				expr = (
					(pl.col("day_date").cast(pl.Datetime) +
					pl.duration(days=column_config["day_to_sum"],
								hours=pl.col(column_config["name"]).dt.hour(),
								minutes=pl.col(column_config["name"]).dt.minute()))
					.cast(self.dtype_dict[column_config["dtype"]])
					.alias(column_config["name"])
				)
				lista_de_expressoes2.append(expr)
			elif column_config["dtype"] not in ["timedelta", "date"]:
				expr = (
					pl.col(column_config["name"])
					.cast(self.dtype_dict[column_config["dtype"]])
					.alias(column_config["name"])
				)
				lista_de_expressoes2.append(expr)

		df_executed = (df_to_execute.select(self.rename_expression)
									.with_columns(lista_de_expressoes)
									.with_columns(lista_de_expressoes2)
									.sort("day_date")
									.select(self.data_schema["cleaned_mrng_cols"]))

		return df_executed
	

	def 
		
class DataTypeChanger:

	def to_date(self, column_name):
		pl.col(column_name).map_elements(lambda x: datetime.strptime(x, "%m-%d-%y").strftime("%Y-%m-%d")).alias(column_name)

class Expressions:

	def __init__(
		self, 
		data_schema:dict,
		):
	
		self.data_schema = data_schema
		self.change = DataTypeChanger()

		# Dict to translate dtype in STRING to dtype in POLARS
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

	def generate_rename_expressions(self, table_id, columns_list):
		if table_id == "morning_v2":
			return [
				pl.col(column_id).alias(column_config["name"])
				for column_id, column_config in self.data_schema[table_id].items()
			]
		else:
			column_dict = {index: column for index, column in enumerate(columns_list)}
			return [
				pl.col(column_dict[int(column_id)]).alias(column_config["name"])
				for column_id, column_config in self.data_schema[table_id].items()
			]
			
	def generate_dtype_cast_expressions(self, table_id):
		return [
			pl.col(column_config["name"]).cast(self.dtype_dict[column_config["dtype"]])
			for column_id, column_config in self.data_schema[table_id].items()
		]
	
	def generate_dtype_formatation_expressions(self):
		pass