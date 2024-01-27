import polars as pl

class DataRefiningProcessor():
	def __init__(self, config):
		self.config = config

		# Path formation
		self.clnd_morning_path = self.config.get_file("cleaned", "mrn_cleaned.parquet")	
		self.rfnd_weight_path  = self.config.get_file("refined", "WM_WeightMeasurements.parquet")	

		# Define tables_relation list
		self.tables_relation = [
			["weight", self.clnd_morning_path, self.rfnd_weight_path]
		]

        # Create an instance of RefiningFunctions for executing refinements
		self.refining_functions = RefiningFunctions()

	# Reading function to read data from the parquet cleaned table
	def reading(self, cleaned_path):
		df_cleaned = pl.read_parquet(cleaned_path)
		return df_cleaned

	# Writing function to write the refined_path as a parquet file in the refined_path
	def writing(self, df_refined, refined_path):
		df_refined.write_parquet(refined_path)

	# Function to execute all the code combined
	def execute(self):
		# Gets the correct relation list from the tables_relation list
		for refine_id, cleaned_path, refined_path in self.tables_relation:
			# Write the refined dataframe in the refined_path
			self.writing(
				# Gets what refinement is going to be executed and the cleaned table necessary to its execution
				self.refining_functions.refine(
					# Read the chosen dataframe from the path given
					self.reading(
						cleaned_path
					),
					refine_id
				),
				refined_path
			)

class RefiningFunctions():
	def __init__(self):

        # Create a dictionary of functions
		self.refine_functions_dict = {
			'weight': self.weight_function
		}

	def weight_function(self, df_cleaned):
		# Perform refinements on the provided dataframe (df_cleaned)

		# Calculate refined columns based on existing columns
		df_refined = df_cleaned\
			.with_columns(
				# Calculate the percentage of fat based on fat_percentage column
				(pl.col("fat_percentage") / 100).alias("fat_percentage"),
				# Calculate the percentage of muscle based on mus_weight and ttl_weight columns
				(pl.col("mus_weight") / pl.col("ttl_weight")).round(3).alias("mus_percentage"),
				# Calculate the weight of fat based on ttl_weight and fat_percentage columns
				(pl.col("ttl_weight") * pl.col("fat_percentage") / 100).round(2).alias("fat_weight"),
			)\
			.with_columns([
				# Calculate the difference between consecutive values for ttl, mus, and fat columns
				(pl.col(f"{x}_weight") - pl.col(f"{x}_weight").shift(1)).fill_null(0.0).alias(f"{x}_diff")
				for x in ["ttl", "mus", "fat"]
			])\
			.with_columns([
				# Create boolean columns indicating whether there is a loss for ttl, mus, and fat
				(pl.when(pl.col(f"{x}_diff") < 0).then(True).otherwise(False)).alias(f"{x}_loss")
				for x in ["ttl", "mus", "fat"]
			])

		# Return the refined dataframe
		return df_refined

	def refine(self, df_cleaned, refine_id):
		# Execute the specified refinement function
		return self.refine_functions_dict[refine_id](df_cleaned)