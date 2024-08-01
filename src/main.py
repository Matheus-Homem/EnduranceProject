import argparse

from src.env.globals import Global
from src.etl.process.orchestrator import ProcessOrchestrator
from src.report.reports import Report


def main():

    parser = argparse.ArgumentParser(description="Script that executes main.py")

    parser.add_argument(
        "--automated",
        type=bool,
        default=False,
        help="Argument identifying script automation",
    )
    parser.add_argument(
        "--date",
        default=None,
        help='Argument identifying script date in the format "YYYYMMDD"',
    )

    args = parser.parse_args()

    automated = args.automated
    script_date = args.date

    Global(exec_date=script_date)

    ProcessOrchestrator().execute(automated=automated)

    Report().daily_publish(send_email=automated)


if __name__ == "__main__":
    main()
