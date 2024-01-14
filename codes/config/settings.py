import os
import json
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

class Config:
	def __init__(self, env):
		self.env = env

		# Group: PATHS VARS
		self.paths = PathsConfig(self.env)

		# Loading secrets defined in the .env file
		load_dotenv(os.path.join(self.paths.project_dir, '.env'))

		# Loading email_settings defined in the JSON file
		email_settings_path = os.path.join(self.paths.config_dir, 'email_settings.json')
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

	def get_file(self, directory, file_name):
		full_dir = directory + "_dir"
		dir_path = getattr(self.paths, full_dir)
		return os.path.join(dir_path, file_name)

class PathsConfig:
	def __init__(self, env):
		self.env = env # Defining environment variable

		self.project_dir = os.path.dirname(os.getcwd()) # Get the parent directory of the current directory (project/)

		# Folders inside main project/ directory
		self.report_dir = os.path.join(self.project_dir, "reports", f"{self.env}") # Path to the env folder inside the reports folder (project/reports/env/)
		self.codes_dir = os.path.join(self.project_dir, "codes") # Path to the codes folder (project/codes/)
		self.files_dir = os.path.join(self.project_dir, "files") # Path to the files folder (project/files/)

		# Folders inside codes/ directory
		self.config_dir = os.path.join(self.codes_dir, "config") # Path to the config folder inside the codes folder (project/codes/config/)
		self.libs_dir = os.path.join(self.codes_dir, "libs") # Path to the libs folder inside the codes folder (project/codes/libs/)

		# Folders inside files/ directory
		self.images_dir = os.path.join(self.files_dir, "images") # Path to the images folder inside the files folder (project/files/images/)
		self.data_dir = os.path.join(self.files_dir, "data") # Path to the data folder inside the files folder (project/files/data/)
		self.misc_dir = os.path.join(self.files_dir, "misc") # Path to the misc folder inside the files folder (project/files/misc/)

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

		