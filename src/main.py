from etl.orchestrator import Orchestrator
from libs.reports import Report

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

	Orchestrator(date_param=script_date).run_pipeline(automated=automated)

	# Everyday generate Daily Report
	Report(date_param=script_date).daily_publish()

if __name__ == "__main__":
	main()