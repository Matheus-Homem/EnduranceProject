import codes.libs.gen_writing as gen
from abc import ABC, abstractmethod
from reportlab.lib.units import inch
from typing import List, Functions

class Partlet(ABC):
	def __init__(self):
		# Initialize Partlet with reference to the main report, configuration, canvas, and initial height
		self.config, self.c, self.height = self.get_params()

		# Initialize Partlet with a empyt list of elements
		self._elements: List[Functions] = []

	def deduce_height(self, value):
		self.height -= value

	def exe_line(self):
		# Draw horizontal line
		h_line = lambda: gen.horizontal_line(self)
		self._elements.append(h_line)

	@abstractmethod
	def daily(self):
		for func in self._elements:
			func()

class Header(Partlet):
	def __init__(self):
		super().__init__()

		self.exe_title()
		self.deduce_height(20)
		self.exe_subtitle()
		self.deduce_height(10)
		self.exe_line()
		self.deduce_height(40)

	def exe_title(self):
		# Title
		title = lambda: gen.centralized_text(self, text="Relatório Diário", pattern="TITLE")
		self._elements.append(title)

	def exe_subtitle(self):
		# Subtitle with date, weekday, and week number
		subtitle_text = f"{self._config.dt.date_fmtd} | {gen.translate_weekday(self._config.dt.week_day)} | Semana: {self._config.dt.week_number}"
		subtitle = lambda: gen.centralized_text(self, text=subtitle_text, pattern="SUBTITLE")
		self._elements.append(subtitle)
		
	def exe_line(self):
		# Draw horizontal line
		h_line = lambda: gen.horizontal_line(self)
		self._elements.append(h_line)

class WeightDiary(Partlet):
	def __init__(self):
		super().__init__()

		self.exe_title()
		self.deduce_height(20)
		self.exe_line()
		self.deduce_height(20)

	def exe_title(self):
		# Subtitle identifing Pesagem (Weighting)
		title = lambda: gen.centralized_text(self, text="Pesagem", pattern="CHAPTER_HEADER")
		self._elements.append(title)

	def daily(self):
		
		gen.centralized_text(self.c,
							 self.height - 20,
							 "Pesagem",
							 "CHAPTER_HEADER")

		# Draw a line under the subtitle
		self.c.line(100, self.height - 27, 500, self.height - 27)

		
		# Adicione uma imagem PNG ao PDF
		plot1_path = self._config.get_partitioned_file(f"WM_{self._config.dt.date}.png")
		self.c.drawImage(plot1_path, inch, inch/4, width=6*inch, height=9.5*inch)

# class Goals(Partlet):
# 	def __init__(self):
# 		pass

# class SleepDiary():
# 	def __init__(self):
# 		pass

# class ReadingDiary(Partlet):
# 	def __init__(self):
# 		pass

# class LearningDiary(Partlet):
# 	def __init__(self):
# 		pass

# class PracticeDiary(Partlet):
# 	def __init__(self):
# 		pass

# class WorkDiary(Partlet):
# 	def __init__(self):
# 		pass

# class StudyDiary(Partlet):
# 	def __init__(self):
# 		pass

# class SymptomDiary(Partlet):
# 	def __init__(self):
# 		pass

# class UpperBodyDiary(Partlet):
# 	def __init__(self):
# 		pass

# class LowerBodyDiary(Partlet):
# 	def __init__(self):
# 		pass

# class NutritionDiary(Partlet):
# 	def __init__(self):
# 		pass

# class SelfcareDiary(Partlet):
# 	def __init__(self):
# 		pass

# class VolunteeringDiary(Partlet):
# 	def __init__(self):
# 		pass

# class RelaxationDiary(Partlet):
# 	def __init__(self):
# 		pass

# class ExcellenceDiary(Partlet):
# 	def __init__(self):
# 		pass

# class MeditationDiary(Partlet):
# 	def __init__(self):
# 		pass