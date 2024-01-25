from datetime import datetime
import polars as pl
import json

class DataCleaningProcessor():
	def __init__(self, config):
		self.config = config

		# Path formation
		self.json_path		   = self.config.get_file("misc",      "rename_columns.json")
		self.raw_morning_path  = self.config.get_file("ingestion", "morning_routine_v2.xlsx")
		self.clnd_morning_path = self.config.get_file("cleaned",   "mrn_cleaned.parquet")
		self.raw_night_path	   = self.config.get_file("ingestion", "night_routine_v2.xlsx")
		self.clnd_night_path   = self.config.get_file("cleaned",   "ngt_cleaned.parquet")

		# Dict to translate dtype in STRING to dtype in POLARS
		self.pl_dtype_dict = {
			"list": pl.List(pl.Utf8),
			"string": pl.Utf8,
			"date": pl.Date,
			"float": pl.Float64,
			"int": pl.Int64,
			"timestamp": pl.Datetime,
			"timedelta": pl.Duration
		}

		# Dict loading the rename_columns.json file
		with open(self.json_path, encoding='utf-8') as f:
			self.rename_columns_dict = json.load(f)

		# Relation of objects variable to manage the table_id, raw_path and cleaning_path
		self.tables_relation = [
			["morning", self.raw_morning_path, self.clnd_morning_path],
			#["night",   self.raw_night_path,   self.clnd_night_path]
		]

		# List of columns that are going to be corrected to microseconds (and further in pl.Duration)
		self.time_cols = ['day_form_time', 'slp_fall', 'pho_time', 'slp_raise', 'slp_duration']

	# Reading function to read data from the excel original file
	def reading(self, raw_path):
		df_raw = pl.read_excel(raw_path)
		return df_raw

	# Cleaning function to rename and correct data formats
	def cleaning(self, df_raw, table_id):
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

		# Corrects the date format from "MM-dd-yy" to "YYYY-MM-dd"
		def correct_date_format(date_var):
			# Convert the date string to a datetime object and format it as "YYYY-MM-dd"
			return datetime.strptime(date_var, "%m-%d-%y").strftime("%Y-%m-%d")

		# Define the expressions of renaming and dtype from the "rename_columns.json"
		def get_expressions(table_key: str):
			# Defining expression to rename columns when called
			rename_expressions = [
				pl.col(column_name).alias(column_config["name"])
				for column_name, column_config in self.rename_columns_dict[table_key].items()
			]
			# Defining expression to correct columns dtype when called
			dtype_expressions = [
				pl.col(column_config["name"]).cast(self.pl_dtype_dict[column_config["dtype"]])
				for column_name, column_config in self.rename_columns_dict[table_key].items()
			]
			return rename_expressions, dtype_expressions

		# Create the correct expression for the table from the table_id
		rename_exp, dtype_exp = get_expressions(table_id)
				
		# Applying expression to rename columns
		renamed_df = df_raw.select(rename_exp)

		# Correction 'day_date' column from "MM-dd-yy" format to "YYYY-MM-dd" format
		formatted_date_df = renamed_df.with_columns(
			pl.col("day_date").map_elements(lambda x: correct_date_format(x)).alias("day_date")
		)

		# Applying 'convert_to_microseconds' function to the selected columns
		corrected_time_df = formatted_date_df.select([
			pl.col(col_name).map_elements(convert_time_to_microseconds).alias(col_name)
			if col_name in self.time_cols
			else col_name
			for col_name in formatted_date_df.columns
		])

		# Applying expression to change columns dtype
		df_cleaned = corrected_time_df.select(dtype_exp)	

		return df_cleaned

	# Writing function to write the df_cleaned as a parquet file in the cleaned_path
	def writing(self, df_cleaned, cleaned_path):
		df_cleaned.write_parquet(cleaned_path)
	
	# Function to execute all the code combined
	def execute(self):
		# Gets the correct relation list from the tables_relation list
		for table_id, raw_path, cleaned_path in self.tables_relation:
			# Write the cleaned dataframe in the cleaned_path
			self.writing(
				# Cleans the correct raw dataframe with the use of table_id
				self.cleaning(
					# Read the chosen dataframe from the path given
					self.reading(raw_path),
					table_id),
				cleaned_path)