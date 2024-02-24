from src.etl.patterns.engine import Engine
from src.etl.cleaning.expressions import ExpressionsGenerator


class CleanerEngine(Engine):

	def __init__(self, data_schema):

		self.data_schema = data_schema
		self.generator = ExpressionsGenerator(data_schema=data_schema)



	def execute(self, df_to_execute, table_id, day_column, mrng_or_night):
		self.rename_expressions = self.generator.rename_expressions(identifier=table_id, columns_list=df_to_execute.columns)
		self.init_dtype_expressions = self.generator.init_dtype_expressions(identifier=table_id)
		self.final_dtype_expressions = self.generator.inal_dtype_expressions(identifier=table_id)

		df_executed = (df_to_execute.select(self.rename_expressions)
									.with_columns(self.init_dtype_expressions)
									.with_columns(self.final_dtype_expressions)
									.sort(day_column)
									.select(self.data_schema[f"{mrng_or_night}_columns"]))
		return df_executed