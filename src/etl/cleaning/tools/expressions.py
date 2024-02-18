import polars as pl

class Expressions:

	def __init__(
		self, 
		table_id:str, 
		dtype_dict:dict, 
		data_schema:dict, 
		df:pl.DataFrame
		):
	
		self.table_id = table_id 
		self.dtype_dict = dtype_dict 
		self.data_schema = data_schema
		self.df = df

		self._generate_rename_expressions()
		self._generate_dtype_expressions()

	def _generate_rename_expressions(self):
		if self.table_id == "morning_v2":
			self.rename_expression = [
				pl.col(column_id).alias(column_config["name"])
				for column_id, column_config in self.data_schema[self.table_id].items()
				]
		elif self.table_id == "morning_v3":
			full_name_dict = {coluna[:3]: coluna for coluna in self.df.columns}
			self.rename_expression = [
				pl.col(full_name_dict.get(column_id[:3])).alias(column_config["name"])
				for column_id, column_config in self.data_schema[self.table_id].items()
				]

	def _generate_dtype_expressions(self):
		self.dtype_expression = [
			pl.col(column_config["name"]).cast(self.dtype_dict[column_config["dtype"]])
			for column_id, column_config in self.data_schema[self.table_id].items()
			]

	def get_expressions(self):
		return self.rename_expression, self.dtype_expression