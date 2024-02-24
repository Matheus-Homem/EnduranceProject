import polars as pl
from datetime import datetime

class FormatConverter:

	@classmethod
	def _to_timedelta(cls, x):
		if x:
			time_converted_to_time64 = datetime.strptime(x, "%H:%M")
			difference_from_midnight = time_converted_to_time64 - datetime.strptime("00:00", "%H:%M")
			total_microseconds = int(difference_from_midnight.total_seconds() * 1e6)
			return total_microseconds
		else:
			return None
		
	@classmethod
	def _to_boolean(cls, x):
		return False if x in [1, "Não"] else (True if x in [2, "Sim"] else None)

	@classmethod
	def _to_date(cls, x):
		return datetime.strptime(x, "%m-%d-%y").strftime("%Y-%m-%d")

	@classmethod
	def _to_timestamp(cls, column_config):
		return (pl.col("day_date").cast(pl.Datetime) +
				pl.duration(days = column_config["day_to_sum"],
							hours = pl.col(column_config["name"]).dt.hour(),
							minutes = pl.col(column_config["name"]).dt.minute()))