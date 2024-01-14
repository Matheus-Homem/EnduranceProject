from report import Report
import section

class DailyReport():
	def __init__(self, configuration):
		self.config = configuration
	
	def generate_report(self):

		## 01. Cria o objeto de canvas
		report = Report(self.config)

		## 02. Cria o cabeçalho | 1
		report.add_section(section.Header())

		## 03. Cria a sessão de objetivos de ontem | 1
		report.add_section(section.Goals(self.config, "yesterday"))

		## 04. Cria a sessão de objetivos de hoje | 1
		report.add_section(section.Goals(self.config, "today"))

		## Quebra de página
		report.skip_page()

		## 05. Cria a sessão de sono | 2
		report.add_section(section.SleepDiary())

		## 06. Cria a sessão de pesagem | 2
		report.add_section(section.WeightDiary())

		## Quebra de página
		report.skip_page()

		## 07. Cria a sessão de leitura | 3
		report.add_section(section.ReadingDiary())

		## 08. Cria a sessao de estudo (aprendizado) | 3
		report.add_section(section.LearningDiary())

		## 09. Cria a sessao de hábitos (prática) | 3
		report.add_section(section.PracticeDiary())

		## Quebra de página
		report.skip_page()
		
		## 10. Cria a sessao de trabalho | 4
		report.add_section(section.WorkDiary())

		## 11. Cria a sessao de estudo técnico | 4
		report.add_section(section.StudyDiary())

		## 12. Cria a sessao de monitoramento de sintomas | 4
		report.add_section(section.SymptomDiary())

		## Quebra de página
		report.skip_page()

		## 13. Cria a sessao de exercícios superiores | 5
		report.add_section(section.UpperBodyDiary())

		## 14. Cria a sessao de exercícios inferiores | 5
		report.add_section(section.LowerBodyDiary())

		## 15. Cria a sessao de nutrição | 5
		report.add_section(section.NutritionDiary())

		## Quebra de página
		report.skip_page()

		## 16. Cria a sessao de autocuidado | 6
		report.add_section(section.SelfcareDiary())

		## 17. Cria a sessao de servidão | 6
		report.add_section(section.VolunteeringDiary())

		## Quebra de página
		report.skip_page()

		## 18. Cria a sessao de desaceleração | 7
		report.add_section(section.RelaxationDiary())

		## 19. Cria a sessao de execelência | 7
		report.add_section(section.ExcellenceDiary())

		## 20. Cria a sessao de meditação | 7
		report.add_section(section.MeditationDiary())

		## 21. Salvamento do relatório
		report.save()

		## 22. Envio do relatório por e-mail
		report.send()

class WeeklyReport():
	pass

class MonthlyReport():
	pass