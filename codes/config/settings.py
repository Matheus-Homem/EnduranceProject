import os
from datetime import date, datetime

class Config:
    def __init__(self, env):
        self.env = env

        # Group: PATHS VARS
        self.paths = PathsConfig(self.env)

        # Group: TODAY DATE VARS
        self.today = DatesConfig("today")

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

        # Build the absolute path to the env folder inside the reports folder (project/files/data/)
        self.directoryData = os.path.join(self.directoryProject, "files", "data")

        # Build the absolute path to the env folder inside the reports folder (project/files/images/)
        self.directoryImages = os.path.join(self.directoryProject, "files", "images")

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

        # Get the current date formatted
        self.dateFormatted = self.date.strftime("%d/%m/%Y")

        # Get the name of the day of the week
        self.weekDay = self.timestamp.strftime("%A")

        # Get the week number of the year
        self.weekNumber = self.timestamp.isocalendar()[1] 