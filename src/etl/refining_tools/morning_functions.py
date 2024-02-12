import polars as pl

class RefiningFunctions():
	def __init__(self):

        # Create a dictionary of functions
		self.refine_functions_dict = {
			'weight': self.weight_function
		}

	def weight_function(self, df_cleaned):
		# Perform refinements on the provided dataframe (df_cleaned)
		print("Refining Engine: Weight Function Started")

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
			]).select(["day_date",
					   "ttl_weight",
					   "ttl_diff",
					   "ttl_loss",
					   "mus_weight",
					   "mus_percentage",
					   "mus_diff",
					   "mus_loss",
					   "fat_weight",
					   "fat_percentage",
					   "fat_diff",
					   "fat_loss",])
		
		print("Refining Engine: Weight Function Finished")

		# Return the refined dataframe
		return df_refined

	def refine(self, df_cleaned, refine_id):
		# Execute the specified refinement function
		return self.refine_functions_dict[refine_id](df_cleaned)