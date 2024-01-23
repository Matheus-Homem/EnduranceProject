from abc import ABC, abstractmethod
from libs.font import translate_weekday
import libs.write_patterns as wrt


class Partlet():
	def __init__(self):
		pass

	@abstractmethod
	def daily_generate(self):
		pass
	
	@abstractmethod
	def weekly_generate(self):
		pass
	
	@abstractmethod
	def monthly_generate(self):
		pass

class Header(Partlet):
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

class Goals(Partlet):
	def __init__(self):
		pass

class SleepDiary():
	def __init__(self):
		pass

class WeightDiary():
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
		pass

class ReadingDiary(Partlet):
	def __init__(self):
		pass

class LearningDiary(Partlet):
	def __init__(self):
		pass

class PracticeDiary(Partlet):
	def __init__(self):
		pass

class WorkDiary(Partlet):
	def __init__(self):
		pass

class StudyDiary(Partlet):
	def __init__(self):
		pass

class SymptomDiary(Partlet):
	def __init__(self):
		pass

class UpperBodyDiary(Partlet):
	def __init__(self):
		pass

class LowerBodyDiary(Partlet):
	def __init__(self):
		pass

class NutritionDiary(Partlet):
	def __init__(self):
		pass

class SelfcareDiary(Partlet):
	def __init__(self):
		pass

class VolunteeringDiary(Partlet):
	def __init__(self):
		pass

class RelaxationDiary(Partlet):
	def __init__(self):
		pass

class ExcellenceDiary(Partlet):
	def __init__(self):
		pass

class MeditationDiary(Partlet):
	def __init__(self):
		pass