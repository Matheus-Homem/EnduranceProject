from src.etl.process.orchestrator import ProcessOrchestrator
from src.report.reports import Report
from src.env.globals import Global

import argparse

def main():

	# Create an ArgumentParser object
	parser = argparse.ArgumentParser(description="Script that executes main.py")

	# Add arguments to the parser
	parser.add_argument('--automated', type=bool, default=False, help='Argument identifying script automation')
	parser.add_argument('--date', default=None, help='Argument identifying script date in the format "YYYYMMDD"')

	# Parse command line arguments
	args = parser.parse_args()

	# Acesse os argumentos
	automated = args.automated
	script_date = args.date

	# Criar uma instância única de Global com base na data de execução
	Global(exec_date=script_date)

	ProcessOrchestrator().execute(automated=automated)

	# Everyday generate Daily Report
	Report().daily_publish(send_email=automated)

if __name__ == "__main__":
	main()