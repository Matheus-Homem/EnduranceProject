from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from libs.report import Report
import libs.partlets as ptt

class DailyReport():
	def __init__(self, configuration):
		self.config = configuration
	
	def generate_report(self):

		# Create a canvas object to generate the PDF
		self.c = canvas.Canvas(
			self.config.get_file("report", f"{self.config.today.date}.pdf"), # File Name
			pagesize=A4
		)

		## 01. Cria o objeto de canvas
		report = Report(self.config, self.c)

		## 02. Cria o cabeçalho | 1
		header = ptt.Header(report, initial_height = 800)
		report.add_partlet(header)

		## 03. Cria a sessão de objetivos de ontem | 1
		#report.add_partlet(ptt.Goals(self.config, "yesterday"))

		## 04. Cria a sessão de objetivos de hoje | 1
		#report.add_partlet(ptt.Goals(self.config, "today"))

		## Quebra de página
		#report.skip_page()

		## 05. Cria a sessão de sono | 2
		#report.add_partlet(ptt.SleepDiary())

		## 06. Cria a sessão de pesagem | 2
		weight = ptt.WeightDiary(report, initial_height = 750)
		report.add_partlet(weight)

		## Quebra de página
		#report.skip_page()

		## 07. Cria a sessão de leitura | 3
		#report.add_partlet(ptt.ReadingDiary())

		## 08. Cria a sessao de estudo (aprendizado) | 3
		#report.add_partlet(ptt.LearningDiary())

		## 09. Cria a sessao de hábitos (prática) | 3
		#report.add_partlet(ptt.PracticeDiary())

		## Quebra de página
		#report.skip_page()
		
		## 10. Cria a sessao de trabalho | 4
		#report.add_partlet(ptt.WorkDiary())

		## 11. Cria a sessao de estudo técnico | 4
		#report.add_partlet(ptt.StudyDiary())

		## 12. Cria a sessao de monitoramento de sintomas | 4
		#report.add_partlet(ptt.SymptomDiary())

		## Quebra de página
		#report.skip_page()

		## 13. Cria a sessao de exercícios superiores | 5
		#report.add_partlet(ptt.UpperBodyDiary())

		## 14. Cria a sessao de exercícios inferiores | 5
		#report.add_partlet(ptt.LowerBodyDiary())

		## 15. Cria a sessao de nutrição | 5
		#report.add_partlet(ptt.NutritionDiary())

		## Quebra de página
		#report.skip_page()

		## 16. Cria a sessao de autocuidado | 6
		#report.add_partlet(ptt.SelfcareDiary())

		## 17. Cria a sessao de servidão | 6
		#report.add_partlet(ptt.VolunteeringDiary())

		## Quebra de página
		#report.skip_page()

		## 18. Cria a sessao de desaceleração | 7
		#report.add_partlet(ptt.RelaxationDiary())

		## 19. Cria a sessao de execelência | 7
		#report.add_partlet(ptt.ExcellenceDiary())

		## 20. Cria a sessao de meditação | 7
		#report.add_partlet(ptt.MeditationDiary())

		## 21. Salvamento do relatório
		report.save("daily")

		## 22. Envio do relatório por e-mail
		#report.send()

class WeeklyReport():
	def __init__(self, configuration):
		self.config = configuration
	
	def generate_report(self):
		pass

class MonthlyReport():
	def __init__(self, configuration):
		self.config = configuration
	
	def generate_report(self):
		pass