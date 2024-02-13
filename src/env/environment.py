import os
from dotenv import load_dotenv

from src.env.paths import PathsConfig
from src.env.calendar import DatesConfig

class EnvironmentConfig:
	def __init__(self, date_param=None):

		# Loading secrets defined in the .env file
		load_dotenv()

		# Verified email
		self.verified_email = os.getenv("VERIFIED_EMAIL")

		# Group: PATHS VARS
		self.paths = PathsConfig()

		# Group: DATE VARS
		self.dt = DatesConfig(date_param)

	def get_verified_email(self):
		return self.verified_email

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
		dir_path = getattr(self.paths, directory)

		# Return the full path to the file by combining the directory path and the file name.
		return os.path.join(dir_path, file_name)

	def get_partitioned_file_path(self, file_name: str) -> str:
		"""
		Create a partitioned directory structure for storing files based on the current date.

		Args:
			directory (str): The name of the base directory where the partitioned structure will be created.
			file_name (str): The name of the file to be stored within the partitioned structure.

		Returns:
			str: The full path to the file within the partitioned directory structure.

		Example:
			Assuming `directory` is "images" and `file_name` is "example.png", and the current date is
			2024-01-28, the function will create the directory structure:
			"{base_directory}/images/2024/01/28/example.png" and return the full path.

		Note:
			This function uses the current date to create a hierarchical directory structure within the
			specified base directory. It checks if the necessary directories exist and creates them if
			they don't.

		"""

		# Get the current date
		date = self.dt.date

		# Extract year, month, and day as strings, ensuring month and day have leading zeros.
		year, month, day = str(date.year), str(date.month).zfill(2), str(date.day).zfill(2)

		# Construct the full path with partitioned directories.
		dir_file_path = os.path.join(self.paths.report, year, month, day, file_name)

		# Check if the directory exists, and create it if necessary.
		if not os.path.exists(os.path.dirname(dir_file_path)):
			os.makedirs(os.path.dirname(dir_file_path))

		# Return the full path to the file within the partitioned structure.
		return dir_file_path