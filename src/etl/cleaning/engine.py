from src.etl.patterns.engine import Engine
from src.etl.cleaning.expressions import ExpressionsGenerator


class CleanerEngine(Engine):

	def __init__(self, cleaning_schema):

		self.cleaning_schema = cleaning_schema
		self.generator = ExpressionsGenerator(cleaning_schema=cleaning_schema)



	def execute(self, df_to_execute, table_id, day_column):
		self.rename_expressions = self.generator.rename_expressions(identifier=table_id)
		self.init_dtype_expressions = self.generator.init_dtype_expressions(identifier=table_id)
		self.final_dtype_expressions = self.generator.final_dtype_expressions(identifier=table_id)

		df_executed = (df_to_execute.select(self.rename_expressions)
									.with_columns(self.init_dtype_expressions)
									.with_columns(self.final_dtype_expressions)
									.sort(day_column))
		return df_executed