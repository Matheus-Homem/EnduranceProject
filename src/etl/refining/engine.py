from src.env.helpers import Paths
import src.etl.refining.tools.morning as mrn
import polars as pl

class DataRefiner:

	def __init__(self):

		# Instanciate Paths
		self.paths = Paths()

		# Path formation
		self.clnd_morning_path = self.paths.get_file_path("cleaned", "mrn_cleaned.parquet")
		self.rfnd_weight_path  = self.paths.get_file_path("refined", "WM_WeightMeasurements.parquet")

		# Define tables_relation list
		self.tables_relation = [
			["weight", self.clnd_morning_path, self.rfnd_weight_path]
		]

        # Create an instance of RefiningFunctions for executing refinements
		self.refining_functions = mrn.RefiningFunctions()

	# Reading function to read data from the parquet cleaned table
	def reading(self, cleaned_path):
		print("Refining Engine: Reading Process Started")
		df_cleaned = pl.read_parquet(cleaned_path)
		print("Refining Engine: Reading Process Finished")
		return df_cleaned

	# Writing function to write the refined_path as a parquet file in the refined_path
	def writing(self, df_refined, refined_path):
		print("Refining Engine: Writing Process Started")
		df_refined.write_parquet(refined_path)
		print("Refining Engine: Writing Process Finished")

	# Function to execute all the code combined
	def execute(self):
		# Gets the correct relation list from the tables_relation list
		for refine_id, cleaned_path, refined_path in self.tables_relation:
			print("\n")
			print(f"Stated Refining Proccess related to {refine_id}")
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