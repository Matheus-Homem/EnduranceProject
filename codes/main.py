from libs.reports import DailyReport
from libs.mailing import send_email
from config.settings import Config
import os

def main():
	config = Config("dev")

	#print(config.paths.filePdf)
	send_email(config, subject="Relatório Diário", email_body="Teste de Relatório")

	#attachment_path=os.path.join(config.paths.directoryPdf, "2024-01-11.pdf")

if __name__ == "__main__":
	main()