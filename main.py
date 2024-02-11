from codes.libs.reports import Report
from etl.orchestrator import execute_orchestration

import time
import argparse

def main():

	# Create an ArgumentParser object
	parser = argparse.ArgumentParser(description="Script that executes main.py")

	# Add arguments to the parser
	parser.add_argument('--automate', type=bool, default=False, help='Argument identifying script automation')
	parser.add_argument('--date', default=None, help='Argument identifying script date in the format "YYYYMMDD"')

	# Parse command line arguments
	args = parser.parse_args()

	# Acesse os argumentos
	automate_execution = args.automate
	script_date = args.date

	while Report()._config_instance.date_validation(automate_execution) :
		print("Databases not updated. Testing again in 1 minute.")
		time.sleep(60) 

	execute_orchestration()

	# Everyday generate Daily Report
	Report().daily_publish(date_str=script_date)

if __name__ == "__main__":
	main()