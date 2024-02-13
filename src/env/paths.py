import os

class Paths:
	def __init__(self):

		# Get the current directory of the script
		self.local = os.path.dirname(os.path.abspath("__file__"))

		# Get the parent directory of the current directory
		self.parent = os.path.dirname(self.local)

		# Folders inside main project/ directory
		self.data		= os.path.join(self.parent, "data")		 # Path to the data folder (project/data/)
		self.outputs	= os.path.join(self.parent,	"outputs")	 # Path to the outputs folder (project/outputs/)
		self.resources	= os.path.join(self.parent,	"resources") # Path to the resources folder (project/resources/)
		self.src		= os.path.join(self.parent,	"src")		 # Path to the src folder (project/src/)

		# Folders inside data/ directory
		self.ingestion	= os.path.join(self.data, "ingestion")	# Path to the ingestion folder inside the data folder (project/data/ingestion/)
		self.cleaned	= os.path.join(self.data, "cleaned")	# Path to the cleaned folder inside the data folder (project/data/cleaned/)
		self.refined	= os.path.join(self.data, "refined")	# Path to the refined folder inside the data folder (project/data/refined/)

		# Folders inside outputs/ directory
		self.report	= os.path.join(self.outputs, "reports")	# Path to the reports folder inside the outputs folder (project/outputs/reports/)

		# Folders inside resources/ directory
		self.json	= os.path.join(self.resources, "json")	# Path to the json folder inside the resources folder (project/resources/json/)

		# Folders inside src/ directory
		self.env	= os.path.join(self.src, "env")		# Path to the env folder inside the src folder (project/src/env/)
		self.etl	= os.path.join(self.src, "etl")		# Path to the etl folder inside the src folder (project/src/etl/)
		self.libs	= os.path.join(self.src, "libs")	# Path to the libs folder inside the src folder (project/src/libs/)

	def get_file_path(self, directory:str, file_name:str) -> str:
		"""
		Get the full path of a file in the specified directory.

		Args:
			directory (str): The name of the directory where the file is located.
			file_name (str): The name of the file you want to retrieve.

		Returns:
			str: The full path to the file.
		"""

		# Get the full directory path using the corresponding attribute.
		dir_path = getattr(self, directory)

		# Return the full path to the file by combining the directory path and the file name.
		return os.path.join(dir_path, file_name)