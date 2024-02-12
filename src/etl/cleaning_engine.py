from datetime import datetime
import polars as pl
import json

class DataCleaner:
	
	def __init__(self, orchestrator_config):
		self.config = orchestrator_config

		# Path formation
		self.json_path		   = self.config.get_file_path("json",      "rename_columns.json")
		self.raw_morning_path  = self.config.get_file_path("ingestion", "morning_routine_v2.xlsx")
		self.clnd_morning_path = self.config.get_file_path("cleaned",   "mrn_cleaned.parquet")
		self.raw_night_path	   = self.config.get_file_path("ingestion", "night_routine_v2.xlsx")
		self.clnd_night_path   = self.config.get_file_path("cleaned",   "ngt_cleaned.parquet")

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

	# Reading function to read data from the excel original file
	def reading(self, raw_path):
		print("Cleaning Engine: Reading Process Started")
		df_raw = pl.read_excel(raw_path)
		print("Cleaning Engine: Reading Process Finished")
		return df_raw

	# Cleaning function to rename and correct data formats
	def cleaning(self, df_raw, table_id):

		# Define the expressions for renaming and dtype from the "rename_columns.json"
		def get_expressions():
			# Defining expression to rename columns when called
			self.rename_exp = [
				pl.col(column_name).alias(column_config["name"])
				for column_name, column_config in self.rename_columns_dict[table_id].items()
			]
			# Defining expression to correct columns dtype when called
			self.dtype_exp = [
				pl.col(column_config["name"]).cast(self.pl_dtype_dict[column_config["dtype"]])
				for column_name, column_config in self.rename_columns_dict[table_id].items()
			]

		# Correction 'day_date' column from "MM-dd-yy" format to "YYYY-MM-dd" format
		def correct_date_fmt(df_raw):
			# Correcting the format of the 'day_date' column from "MM-dd-yy" to "YYYY-MM-dd"
			df1 = df_raw.with_columns(
				# Using the map function to apply date formatting to each element in the 'day_date' column
				pl.col("day_date").map_elements(lambda x: datetime.strptime(x, "%m-%d-%y").strftime("%Y-%m-%d")).alias("day_date")
			)
			return df1

		def correct_duration_fmt(df1, cols_list):
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
				if col_name in cols_list
				else col_name
				for col_name in df1.columns
			])

			# Applying expression to change columns dtype
			df3 = (df2.select(self.dtype_exp)
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

		#########################
		### Starting Cleaning ###
		#########################

		print("Cleaning Engine: Cleaning Process Started")

		# List of columns that are going to be corrected to microseconds (and further in pl.Duration)
		time_cols = ['day_form_time', 'slp_fall', 'pho_time', 'slp_raise', 'slp_duration']

		# Expressions creation
		get_expressions()

		# Applying expression to rename columns
		renamed_df = df_raw.select(self.rename_exp)

		# Apply correction functions
		df_cleaned = correct_datetime_fmt(
						correct_duration_fmt(
							correct_date_fmt(
								renamed_df
							),
							time_cols
						)
					)
		
		print("Cleaning Engine: Cleaning Process Finished")

		return df_cleaned

	# Verification function to filter the user email address from the raw file
	def validating(self, df_cleaned):
		print("Cleaning Engine: Validating Process Started")
		# Filter the DataFrame based on the 'email_confirmation' column matching the configured 'verified_email'.
		df_validated = df_cleaned.filter(pl.col("email_confirmation") == self.config.get_verified_email())
		print("Cleaning Engine: Validating Process Finished")
		return df_validated

	# Writing function to write the df_cleaned as a parquet file in the cleaned_path
	def writing(self, df_validated, cleaned_path):
		print("Cleaning Engine: Writing Process Started")
		df_validated.write_parquet(cleaned_path)
		print("Cleaning Engine: Writing Process Finished")
	
	# Function to execute all the code combined
	def execute(self):
		# Gets the correct relation list from the tables_relation list
		for table_id, raw_path, cleaned_path in self.tables_relation:
			# Write the validated dataframe in the cleaned_path
			self.writing(
				# Validate the cleaned dataframe to contain only the correct user answers
				self.validating(
					# Cleans the correct raw dataframe with the use of table_id
					self.cleaning(
						# Read the chosen dataframe from the path given
						self.reading(
							raw_path
						),
						table_id
					)
				),
				
				cleaned_path
			)