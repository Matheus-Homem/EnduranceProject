from src.env.paths import Paths

import os
from datetime import datetime, date

class Calendar:
	def __init__(self, date_param=None):

		# Convert the input string to a datetime object
		self.date = datetime.strptime(date_param, "%Y%m%d") if date_param != None else date.today()
		self.timestamp = datetime.combine(self.dt, datetime.min.time())

		# Calculate other variables
		self.ingestion = self.dt.strftime("%m-%d-%y") # Get the date as in ingestion layer
		self.dt_fmtd = self.dt.strftime("%d/%m/%Y") # Get the formatted date
		self.week_day = self.timestamp.strftime("%A") # Get the name of the day of the week
		self.week_number = self.timestamp.isocalendar()[1] # Get the week number of the year

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

		# Extract year, month, and day as strings, ensuring month and day have leading zeros.
		year, month, day = str(self.date.year), str(self.date.month).zfill(2), str(self.date.day).zfill(2)

		# Construct the full path with partitioned directories.
		dir_file_path = os.path.join(Paths().report, year, month, day, file_name)

		# Check if the directory exists, and create it if necessary.
		if not os.path.exists(os.path.dirname(dir_file_path)):
			os.makedirs(os.path.dirname(dir_file_path))

		# Return the full path to the file within the partitioned structure.
		return dir_file_path