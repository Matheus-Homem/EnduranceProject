from src.etl.patterns import Orchestrator
import src.etl.refining.tools.morning as mrn


class RefinerOrchestrator(Orchestrator):

	def __init__(self):
		super().__init__()

		self.process = "REFINING"

		# Path formation
		## Cleaned Paths
		# self.clnd_mrn_cold_path	= self.paths.get_file_path("cleaned",   "mrn_cleaned_cold.parquet")
		self.clnd_mrn_hot_path	= self.paths.get_file_path("cleaned",   "mrn_cleaned_hot.parquet")
		# self.clnd_night_path	= self.paths.get_file_path("cleaned",   "ngt_cleaned.parquet")
		# self.clnd_morning_path = self.paths.get_file_path("cleaned", "mrn_cleaned.parquet")
		self.rfnd_weight_path  = self.paths.get_file_path("refined", "WM_WeightMeasurements.parquet")

		# Define tables_relation list
		self.tables_relation = [
			["weight", self.clnd_mrn_hot_path, self.rfnd_weight_path]
		]

		# Create an instance of RefiningFunctions for executing refinements
		self.refining_functions = mrn.RefiningFunctions()

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
						file_format="parquet",
						file_path=cleaned_path
					),
					refine_id=refine_id
				),
				file_path=refined_path
			)