# import unittest

# from src.etl.definitions import ProccessingType
# from src.etl.pipeline.execute import execute_pipeline
# from src.etl.pipeline.properties import PipelineProperties
# from src.etl.readers.database import DatabaseReader
# from src.etl.readers.delta import DeltaReader
# from src.etl.readers.json import JsonReader
# from src.etl.writers.delta import DeltaWriter
# from src.etl.writers.json import JsonWriter
# from src.shared.database.tables import LocalTest, MorningData


# class TestPipeline(unittest.TestCase):

#     def test_bronze_pipeline(self):
#         bronze_pipeline = PipelineProperties(
#             reader=DatabaseReader(table=MorningData),
#             writer=JsonWriter(),
#             processing_type=ProccessingType.FULL,
#         )
#         result = execute_pipeline(bronze_pipeline)
#         self.assertIsNone(result)

#     def test_silver_pipeline(self):
#         silver_pipeline = PipelineProperties(
#             reader=JsonReader(),
#             writer=DeltaWriter(),
#             processing_type=ProccessingType.FULL,
#         )
#         result = execute_pipeline(silver_pipeline)
#         self.assertIsNone(result)

#     def test_gold_pipeline(self):
#         gold_pipeline = PipelineProperties(
#             reader=DeltaReader(),
#             writer=DeltaWriter(),
#             processing_type=ProccessingType.INCREMENTAL,
#         )
#         result = execute_pipeline(gold_pipeline)
#         self.assertIsNone(result)


# if __name__ == "__main__":
#     unittest.main()
