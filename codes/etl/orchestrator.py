from etl.data_cleaning_processor import DataCleaningProcessor
from etl.data_refining_processor import DataRefiningProcessor

def execute_orchestration():
	DataCleaningProcessor.execute()
	DataRefiningProcessor.execute()