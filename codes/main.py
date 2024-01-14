from libs.reports import MonthlyReport, WeeklyReport, DailyReport
from config.settings import Config

def main():
	config = Config("dev")

	today = config.today.date

	#send_email(config, subject="Relatório Diário", email_body="Teste de Relatório")

	if today.day == 1:
		MonthlyReport(config).generate_report()
	elif today.weekday() == 0:
		WeeklyReport(config).generate_report()
	else:
		DailyReport(config).generate_report()

if __name__ == "__main__":
	main()