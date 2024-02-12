from datetime import datetime, date

class DatesConfig:
	def __init__(self, date_str=None):

		# Convert the input string to a datetime object
		self.dt = datetime.strptime(date_str, "%Y%m%d") if date_str != None else date.today()
		self.timestamp = datetime.combine(self.dt, datetime.min.time())

		# Calculate other variables
		self.ingestion = self.dt.strftime("%m-%d-%y") # Get the date as in ingestion layer
		self.dt_fmtd = self.dt.strftime("%d/%m/%Y") # Get the formatted date
		self.week_day = self.timestamp.strftime("%A") # Get the name of the day of the week
		self.week_number = self.timestamp.isocalendar()[1] # Get the week number of the year