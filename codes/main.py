from libs.reports import DailyReport
from config.settings import Config

def main():
    config = Config("dev")

    print(config.paths.directoryPdf)
    print(config.paths.fileMorningData)
    print(config.today.weekNumber)

if __name__ == "__main__":
    main()