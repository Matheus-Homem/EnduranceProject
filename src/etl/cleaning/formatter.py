import polars as pl
from datetime import datetime

class Formatter:

	@classmethod
	def cast_to_timedelta(cls, x):
		if x:
			time_converted_to_time64 = datetime.strptime(x, "%H:%M")
			difference_from_midnight = time_converted_to_time64 - datetime.strptime("00:00", "%H:%M")
			total_microseconds = int(difference_from_midnight.total_seconds() * 1e6)
			return total_microseconds
		else:
			return None
		
	@classmethod
	def cast_to_boolean(cls, x):
		return False if x in [1, "Não"] else (True if x in [2, "Sim"] else None)

	@classmethod
	def cast_to_date(cls, x):
		try:
			parsed_date = datetime.strptime(x, "%m-%d-%y")
			return parsed_date.strftime("%Y-%m-%d")
		except ValueError:
			return x

	@classmethod
	def cast_to_timestamp(cls, config):
		return (pl.col("day_date").cast(pl.Datetime) +
				pl.duration(days = config["day_to_sum"],
							hours = pl.col(config["rename_to"]).dt.hour(),
							minutes = pl.col(config["rename_to"]).dt.minute()))
	
	@classmethod
	def rename(cls, old_name, config):
		return pl.col(old_name).alias(config["rename_to"])
	
	@classmethod
	def concatenate_two(cls, old_name, config):
		col1 = f"{old_name} [X_%]"
		col2 = f"{old_name} [_X%]"
		return (pl.col(col1) + pl.col(col2)).alias(config["rename_to"])
	
	@classmethod
	def concatenate_four(cls, old_name, config):
		col1 = f"{old_name} [X_.__ {config['suffix']}]"
		col2 = f"{old_name} [_X.__ {config['suffix']}]"
		col3 = f"{old_name} [__.X_ {config['suffix']}]"
		col4 = f"{old_name} [__._X {config['suffix']}]"
		return (pl.col(col1) + pl.col(col2) + pl.lit(".") + pl.col(col3) + pl.col(col4)).alias(config["rename_to"])