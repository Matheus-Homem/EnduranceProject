import libs.write_patterns as wrt
from libs.font import translate_weekday

class Partlet():
	def __init__(self):
		pass

class Header():
	def __init__(self, report, initial_height):
		# Initialize Header with reference to the main report, configuration, canvas, and initial height
		self.config = report.config  # Configuration object from the main report
		self.c = report.c  # Canvas object from the main report
		self.up_start = initial_height  # Initial height for positioning elements

	def daily_generate(self):
		# Generate the header partlet with centralized text and a line
		# Title
		wrt.centralized_text(self.c,
							 self.up_start,
							 "Relatório Diário",
							 "TITLE")

		# Subtitle with date, weekday, and week number
		wrt.centralized_text(self.c,
							 self.up_start - 20,
							 f"{self.config.today.date_fmtd} | {translate_weekday(self.config.today.week_day)} | Semana: {self.config.today.week_number}",
							 "SUBTITLE")

		# Draw a line under the subtitle
		self.c.line(100, self.up_start - 25, 500, self.up_start - 25)	

class Goals():
	def __init__(self, configuration, goal_date):
		self.config = configuration
		self.date = goal_date
		pass

class SleepDiary():
	def __init__(self):
		pass

class WeightDiary():
	def __init__(self):
		pass

class ReadingDiary():
	def __init__(self):
		pass

class LearningDiary():
	def __init__(self):
		pass

class PracticeDiary():
	def __init__(self):
		pass

class WorkDiary():
	def __init__(self):
		pass

class StudyDiary():
	def __init__(self):
		pass

class SymptomDiary():
	def __init__(self):
		pass

class UpperBodyDiary():
	def __init__(self):
		pass

class LowerBodyDiary():
	def __init__(self):
		pass

class NutritionDiary():
	def __init__(self):
		pass

class SelfcareDiary():
	def __init__(self):
		pass

class VolunteeringDiary():
	def __init__(self):
		pass

class RelaxationDiary():
	def __init__(self):
		pass

class ExcellenceDiary():
	def __init__(self):
		pass

class MeditationDiary():
	def __init__(self):
		pass