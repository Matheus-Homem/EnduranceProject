from etl.data_cleaning_processor import DataCleaningProcessor
from libs.reports import (MonthlyReport, 
						  WeeklyReport, 
						  DailyReport)
from config.settings import Config

def main():
	config = Config("dev")

	today = config.today.date

	# Data cleaning executions
	DataCleaningProcessor(config).execute()

	#send_email(config, subject="Relatório Diário", email_body="Teste de Relatório")

	# Generate Monthly Report if it's the first day of the month
	if today.day == 1:
		MonthlyReport(config).generate_report()
	
	# Generate Weekly Report if it's Monday
	if today.weekday() == 0:
		WeeklyReport(config).generate_report()
	
	# Always generate Daily Report
	DailyReport(config).generate_report()

if __name__ == "__main__":
	main()