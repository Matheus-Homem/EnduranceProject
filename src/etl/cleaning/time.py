from datetime import datetime
import polars as pl

class DateCleaner:
	
	def __init__(self):
		self.time_cols = ['day_form_time', 'slp_fall', 'pho_time', 'slp_raise', 'slp_duration']

	def exec(self):
		wc1 = pl.col("day_date").map_elements(lambda x: datetime.strptime(x, "%m-%d-%y").strftime("%Y-%m-%d")).alias("day_date")


	# Correction 'day_date' column from "MM-dd-yy" format to "YYYY-MM-dd" format
	def correct_date_fmt(df_raw):
		# Correcting the format of the 'day_date' column from "MM-dd-yy" to "YYYY-MM-dd"
		df1 = df_raw.with_columns(
			# Using the map function to apply date formatting to each element in the 'day_date' column
			pl.col("day_date").map_elements(lambda x: datetime.strptime(x, "%m-%d-%y").strftime("%Y-%m-%d")).alias("day_date")
		)
		return df1

	# Function to convert time string to microseconds
	def convert_time_to_microseconds(self, time_str):
		if time_str:
			# Convert time string to time64 type
			time_micros = pl.lazy.expr(time_str).to_time64()
			# Calculate difference from midnight
			difference = time_micros - pl.lazy.expr("00:00").to_time64()
			return difference
		else:
			return None

	# Function to correct the duration format
	def correct_duration_fmt(self, df):
		# Apply time conversion function to selected columns
		for col_name in df.columns:
			if col_name in self.time_cols:
				# Use map function to apply conversion to each element in column
				df = df.with_column(col_name, pl.map(
					lambda x: self.convert_time_to_microseconds(x), col_name))
		
		# Select desired data types and sort by day_date
		df = df.select(self.dtype_expression).sort("day_date")
		
		return df

	# Function to correct the duration format
	def correct_duration_fmt(self, df):
		# Apply time conversion function to selected columns
		for col_name in df.columns:
			if col_name in self.time_cols:
				# Use map_elements function to apply conversion to each element in column
				df = df.with_column(
					col_name,
					pl.map_elements(self.convert_time_to_microseconds, col_name)
				)

	def correct_duration_fmt(df1):
		# Converts a time string in the "HH:MM" format to microseconds
		def convert_time_to_microseconds(time_str):
			# Check if the input time string is not None
			if time_str is not None:
				# Convert the time string to a datetime object
				time_datetime = datetime.strptime(time_str, "%H:%M")
				# Calculate the time difference from midnight and convert to microseconds
				difference = time_datetime - datetime.strptime("00:00", "%H:%M")
				microseconds = int(difference.total_seconds() * 1e6)
				return microseconds
			else:
				return None

		# Applying 'convert_to_microseconds' function to the selected columns
		df2 = df1.select([
			pl.col(col_name).map_elements(convert_time_to_microseconds).alias(col_name)
			if col_name in self.time_cols
			else col_name
			for col_name in df1.columns
		])

		# Applying expression to change columns dtype
		df3 = (df2.select(self.dtype_expression)
					.sort("day_date"))

		return df3

	def correct_datetime_fmt(df3):
		# Adaptacao do campo day_form_time para conter a data de day_date + 1, com o horario e os minutos de day_form_time
		df4 = df3.with_columns(
			[
				(pl.col("day_date").cast(pl.Datetime) + pl.duration(days=1, hours=pl.col("day_form_time").dt.hour(), minutes=pl.col("day_form_time").dt.minute())).alias("day_form_time"),
				(pl.col("day_date").cast(pl.Datetime) + pl.duration(days=0, hours=pl.col("slp_fall").dt.hour(),		 minutes=pl.col("slp_fall").dt.minute())).alias("slp_fall"),
				(pl.col("day_date").cast(pl.Datetime) + pl.duration(days=1, hours=pl.col("slp_raise").dt.hour(),	 minutes=pl.col("slp_raise").dt.minute())).alias("slp_raise")
			]
		)

		return df4

