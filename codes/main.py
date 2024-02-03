from codes.libs.reports import Report
from etl.orchestrator import execute_orchestration

import time
import argparse

def main():

	# Crie um objeto ArgumentParser
	parser = argparse.ArgumentParser(description="Script que executa main.py")

	# Adicione argumentos ao parser
	parser.add_argument('--automate', type=bool, default=False, help='Argumento identificando a automação do script')
	parser.add_argument('--date', default=None, help='Argumento identificando a data do script no formato "YYYYMMDD"')

	# Parse os argumentos da linha de comando
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