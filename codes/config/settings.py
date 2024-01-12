import os
from datetime import date, datetime, timedelta
from dotenv import load_dotenv

class Config:
	def __init__(self, env):
		self.env = env

		# Group: PATHS VARS
		self.paths = PathsConfig(self.env)

		# Loading secrets defined in the .env file
		load_dotenv(os.path.join(self.paths.directoryMisc, '.env'))

		# Group: TODAY DATE VARS
		self.today = DatesConfig("today")

		# Group: YESTERDAY'S DATE VARS
		self.yesterday = DatesConfig("yesterday")
		
		# Group: SMTP VARS (MAILING)
		self.smtp = MailConfig(
			server=os.getenv("SMTP_SERVER"), 
			port=587, 
			username=os.getenv("SMTP_USER"), 
			password=os.getenv("SMTP_PASSWORD"), 
			recipient=os.getenv("SMTP_RECIPIENT")
		)

class PathsConfig:
	def __init__(self, env):
		self.env = env

		# Get the current directory of the script (project/codes/)
		self.file = os.getcwd()

		# Get the parent directory of the current directory (project/)
		self.directoryProject = os.path.dirname(self.file)

		# Build the absolute path to the env folder inside the reports folder (project/reports/env/)
		self.directoryPdf = os.path.join(self.directoryProject, "reports", f"{self.env}")

		# Build the absolute path to the files folder (project/files/)
		self.directoryFiles = os.path.join(self.directoryProject, "files")

		# Build the absolute path to the data folder inside the files folder (project/files/data/)
		self.directoryData = os.path.join(self.directoryProject, "files", "data")

		# Build the absolute path to the images folder inside the files folder (project/files/images/)
		self.directoryImages = os.path.join(self.directoryProject, "files", "images")

		# Build the absolute path to the misc folder inside the files folder (project/files/misc/)
		self.directoryMisc = os.path.join(self.directoryProject, "files", "misc")

		# Build the path to the pdf file to be generated
		self.filePdf = os.path.join(self.directoryPdf, f"{date.today()}.pdf")

		# Build the path to the morning_routine data file
		self.fileMorningData = os.path.join(self.directoryData, "morning_routine_v2.xlsx")

		# Build the path to the night_routine data file
		self.fileNightData = os.path.join(self.directoryData, "night_routine_v2.xlsx")

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

		self.dateFormatted = self.date.strftime("%d/%m/%Y") # Get the current date formatted
		self.weekDay = self.timestamp.strftime("%A") # Get the name of the day of the week
		self.weekNumber = self.timestamp.isocalendar()[1] # Get the week number of the year

class MailConfig:
	def __init__(self, server, port, username, password, recipient):
		# Gmail SMTP Server Settings
		self.server = server  # SMTP server address for Gmail
		self.port = port  # Port number for Gmail's SMTP server
		self.username = username  # Your Gmail email address
		self.password = password  # Your Gmail email password

		# Mailing Recipient
		self.recipient = recipient  # Email address of the recipient

		