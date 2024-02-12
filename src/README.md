# Directory Organization: *src*

The `src` directory comprises essential **code files** necessary for the correct execution.

It is structured as follows:

- `src/main.py`: Main execution file used to initiate the process comprehensively;

### env

- `src/env/calendar.py`: Script containing a class with attributes related to date, such as formatted date, name of the day of the week, and week number in the year;
- `src/env/email.py`: Script containing a class with information like the username, password, and recipient needed for email sending via the SMTP server;
- `src/env/paths.py`: Script containing the class with directory path information;
- `src/env/environment.py`: Principal script in the `env` directory. The class created in this script instantiates all other classes created in this directory, allowing for complete usage of centralized date, path, and email information through this configuration class;

### etl

- `src/etl/orchestrator.py`: Script containing the class that orchestrates the entire script automation validation pipeline and also the data handling through the classes created in this same directory;
- `src/etl/cleaning_engine.py`: Script containing the class responsible for "cleaning" the data from the ingestion layer to the cleaned layer;
- `src/etl/refining_engine.py`: Script containing the class responsible for "refining" the data from the cleaned layer to the refined layer with the assistance of functions from scripts contained in the `src/etl/refining_tools/` folder;
- `src/etl/refining_tools/morning_functions.py`: Script containing refinement functions to aid in the refinement of each particular topic;

### libs

- `src/libs/utils/scribe.py`: Script containing the class that assists in PDF writing;
- `src/libs/mailing/`: Script responsible for composing and sending emails through SMTP connection;
- `src/libs/partlets/`: Script responsible for assembling the individual parts of the PDF report;
- `src/libs/reports/`: Script responsible for assembling the report itself and organizing its generation and sending using the other libraries in this directory.