import os
import json
import polars as pl
from datetime import datetime, date
from dotenv import load_dotenv

class Config:
	def __init__(self):

		# Loading secrets defined in the .env file
		load_dotenv()

		# Verified email
		self.verified_email = os.getenv("VERIFIED_EMAIL")

		# Group: PATHS VARS
		self.paths = PathsConfig(os.getenv("PATH_TO_SETTINGS"))

		# Loading email_settings defined in the JSON file
		email_settings_path = os.path.join(self.paths.misc, 'email_settings.json')
		with open(email_settings_path, 'r') as f:
			email_settings = json.load(f)

		# Group: SMTP VARS (MAILING)
		self.smtp = MailConfig(
			username=email_settings["SMTP_USERNAME"], 
			password=os.getenv("SMTP_PASSWORD"), 
			recipient=email_settings["SMTP_RECIPIENT"]
		)

	def init_DatesConfig(self, date:str|None=None):
		# Group: DATE VARS
		self.dt = DatesConfig(date)

	def get_file(self, directory:str, file_name:str) -> str:
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

	def get_partitioned_file(self, file_name: str) -> str:
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
	
	def date_validation(self, automate:bool = False):
		if automate == True:
			df_raw_morning = pl.read_excel(self.get_file("ingestion", "morning_routine_v2.xlsx"))
			df_raw_night = pl.read_excel(self.get_file("ingestion", "night_routine_v2.xlsx"))
			morning_true = str(self.dt.strftime("%m-%d-%y")) == df_raw_morning.select(df_raw_morning.columns[2])[-1]
			night_true = str(self.dt.strftime("%m-%d-%y")) == df_raw_night.select(df_raw_night.columns[2])[-1]
			if morning_true  and night_true:
				return True
			else:
				return False
		elif automate == False:
			return False

class PathsConfig:
	def __init__(self, settings_path):
		
		# Parent Folder
		self.parent = os.path.dirname(os.path.dirname(os.path.dirname(settings_path)))

		# Folders inside main project/ directory
		self.report = os.path.join(self.parent, "reports") # Path to the reports folder (project/reports/)
		self.codes	= os.path.join(self.parent,	"codes")   # Path to the codes folder (project/codes/)
		self.files	= os.path.join(self.parent,	"files")   # Path to the files folder (project/files/)

		# Folders inside codes/ directory
		self.config = os.path.join(self.codes, "config") # Path to the config folder inside the codes folder (project/codes/config/)
		self.libs	= os.path.join(self.codes, "libs")	 # Path to the libs folder inside the codes folder (project/codes/libs/)

		# Folders inside files/ directory
		self.images = os.path.join(self.files, "images") # Path to the images folder inside the files folder (project/files/images/)
		self.data	= os.path.join(self.files, "data")	 # Path to the data folder inside the files folder (project/files/data/)
		self.misc	= os.path.join(self.files, "misc")	 # Path to the misc folder inside the files folder (project/files/misc/)

		# Folders inside data/ directory
		self.ingestion = os.path.join(self.data, "ingestion") # Path to the ingestion folder inside the files folder (project/files/ingestion/)
		self.cleaned   = os.path.join(self.data, "cleaned")	  # Path to the cleaned folder inside the files folder (project/files/cleaned/)
		self.refined   = os.path.join(self.data, "refined")	  # Path to the refined folder inside the files folder (project/files/refined/)

class DatesConfig:
	def __init__(self, date_str):

		# Convert the input string to a datetime object
		self.dt = datetime.strptime(date_str, "%Y%m%d") if date_str != None else date.today()
		self.timestamp = datetime.combine(self.dt, datetime.min.time())

		# Calculate other variables
		self.dt_fmtd = self.dt.strftime("%d/%m/%Y") # Get the current date formatted
		self.week_day = self.timestamp.strftime("%A") # Get the name of the day of the week
		self.week_number = self.timestamp.isocalendar()[1] # Get the week number of the year

class MailConfig:
	def __init__(self, username, password, recipient):
		# Gmail SMTP Server Settings
		self.server = "smtp.gmail.com"  # SMTP server address for Gmail
		self.port = 587  # Port number for Gmail's SMTP server
		self.username = username  # Your Gmail email address
		self.password = password  # Your Gmail email password

		# Mailing Recipient
		self.recipient = recipient  # Email address of the recipient