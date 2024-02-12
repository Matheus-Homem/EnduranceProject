import os

class PathsConfig:
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

