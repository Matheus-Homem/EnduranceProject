import os
import json
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

class Config:
	def __init__(self, env):
		self.env = env

		# Loading secrets defined in the .env file
		load_dotenv()

		# Verified email
		self.verified_email = os.getenv("VERIFIED_EMAIL")

		# Group: PATHS VARS
		self.paths = PathsConfig(self.env, os.getenv("PATH_TO_SETTINGS"))

		# Loading email_settings defined in the JSON file
		email_settings_path = os.path.join(self.paths.misc, 'email_settings.json')
		with open(email_settings_path, 'r') as f:
			email_settings = json.load(f)

		# Group: TODAY DATE VARS
		self.today = DatesConfig("today")

		# Group: YESTERDAY'S DATE VARS
		self.yesterday = DatesConfig("yesterday")
		
		# Group: SMTP VARS (MAILING)
		self.smtp = MailConfig(
			username=email_settings["SMTP_USERNAME"], 
			password=os.getenv("SMTP_PASSWORD"), 
			recipient=email_settings["SMTP_RECIPIENT"]
		)

	def get_file(self, directory:str, file_name:str) -> str:
		"""
		Get the full path of a file in the specified directory.

		Args:
			directory (str): The name of the directory where the file is located.
			file_name (str): The name of the file you want to retrieve.

		Returns:
			str: The full path to the file.
		"""
		# Concatenate the suffix "" to the directory name to get the corresponding attribute.
		#full = directory + ""

		# Get the full directory path using the corresponding attribute.
		dir_path = getattr(self.paths, directory)

		# Return the full path to the file by combining the directory path and the file name.
		return os.path.join(dir_path, file_name)

class PathsConfig:
	def __init__(self, env, settings_path):
		self.env = env  # Defining environment variable

		# Diretório pai
		self.parent = os.path.dirname(os.path.dirname(os.path.dirname(settings_path)))

		# Folders inside main project/ directory
		self.report = os.path.join(self.parent, "reports", f"{self.env}") # Path to the env folder inside the reports folder (project/reports/env/)
		self.codes	= os.path.join(self.parent,	"codes")				  # Path to the codes folder (project/codes/)
		self.files	= os.path.join(self.parent,	"files")				  # Path to the files folder (project/files/)

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
		
		# Variable assignment based on the input string
		if date_str == "today":
			# Get the current date as date and as timestamp
			self.date = date.today()
			self.timestamp = datetime.now()
		elif date_str == "yesterday":
			# Get yesterday's date as date and as timestamp
			self.date = date.today() - timedelta(days=1)
			self.timestamp = datetime.combine(self.date, datetime.min.time())\

		self.date_fmtd = self.date.strftime("%d/%m/%Y") # Get the current date formatted
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

		