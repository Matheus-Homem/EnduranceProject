import unittest
from unittest.mock import MagicMock, call, patch

from src.etl.core.cleaning import CleaningEngine
from src.etl.core.definitions import EngineType, Format, Layer, RefinementType
from src.etl.core.extraction import ExtractionEngine
from src.etl.core.io.manager import IOManager
from src.etl.core.pipeline import Pipeline
from src.etl.core.refinement import RefinementEngine


class TestPipeline(unittest.TestCase):

    def test_extract(self):
        # Preparation
        reader_manager = MagicMock(spec=IOManager)
        engine = MagicMock(spec=ExtractionEngine)
        writer_manager = MagicMock(spec=IOManager)
        reader_manager.format = Format.JDBC
        reader = reader_manager.get_handler.return_value
        writer = writer_manager.get_handler.return_value

        # Execution
        pipeline = Pipeline(
            reader=reader_manager,
            engine=engine,
            writer=writer_manager,
        )
        pipeline._extract(table_to_read="element_entries", table_to_write="entries")

        # Assertion
        reader.read.assert_called_once_with(table_name="element_entries")
        df = reader.read.return_value

        engine.process.assert_called_once_with(df)
        df = engine.process.return_value

        writer.write.assert_called_once_with(dataframe=df, table_name="entries", partition_cols=["year", "month", "day"])

    @patch("src.etl.core.pipeline.PipelineUtils.split_dataframe")
    @patch("src.etl.core.pipeline.PipelineUtils.get_subset_table_name")
    def test_clean(self, mock_get_subset_table_name, mock_split_dataframe):
        # Preparation
        ## Pipeline configuration with mocks
        reader_manager = MagicMock(spec=IOManager)
        engine = MagicMock(spec=CleaningEngine)
        writer_manager = MagicMock(spec=IOManager)
        reader = reader_manager.get_handler.return_value
        writer = writer_manager.get_handler.return_value
        reader_manager.format = Format.PARQUET

        ## Side effects configuration
        subset1 = MagicMock()
        subset2 = MagicMock()
        processed_table1 = MagicMock()
        processed_table2 = MagicMock()
        mock_split_dataframe.return_value = [subset1, subset2]
        mock_get_subset_table_name.side_effect = ["subset_table1", "subset_table2"]
        engine.process.side_effect = [processed_table1, processed_table2]

        # Execution
        pipeline = Pipeline(
            reader=reader_manager,
            engine=engine,
            writer=writer_manager,
        )
        pipeline._clean(table_to_read="entries")

        # Assertions
        ## Assert read
        reader.read.assert_called_once_with(table_name="entries")
        df = reader.read.return_value

        ## Assert split
        mock_split_dataframe.assert_called_once_with(dataframe=df, column_to_split=pipeline.column_separator)
        expected_get_subset_calls = [
            call(dataframe=subset1, subset_col_id=pipeline.column_separator),
            call(dataframe=subset2, subset_col_id=pipeline.column_separator),
        ]
        mock_get_subset_table_name.assert_has_calls(expected_get_subset_calls, any_order=False)

        ## Assert process
        expected_process_calls = [call(subset1), call(subset2)]
        engine.process.assert_has_calls(expected_process_calls, any_order=False)
        assert engine.process.call_count == 2

        ## Assert write
        expected_write_calls = [
            call(dataframe=processed_table1, table_name="subset_table1"),
            call(dataframe=processed_table2, table_name="subset_table2"),
        ]
        writer.write.assert_has_calls(expected_write_calls, any_order=False)
        assert writer.write.call_count == 2

    def test_refine_summary_dataframe(self):
        # Preparation
        ## Pipeline configuration with mocks
        reader_manager = MagicMock(spec=IOManager)
        engine = MagicMock(spec=RefinementEngine)
        writer_manager = MagicMock(spec=IOManager)
        reader = reader_manager.get_handler.return_value
        writer = writer_manager.get_handler.return_value
        engine.type = EngineType.REFINEMENT
        reader_manager.format = Format.DELTA
        reader.list_delta_tables.return_value = ["cleaned_table1", "cleaned_table2"]

        ## Side effects configuration
        df_cleaned_1 = MagicMock()
        df_cleaned_2 = MagicMock()
        df_processed_1 = MagicMock()
        df_processed_2 = MagicMock()
        df_refined = MagicMock()
        reader.read.side_effect = [df_cleaned_1, df_cleaned_2]
        engine.process.side_effect = [df_processed_1, df_processed_2]
        engine.union_dataframes.return_value = df_refined

        # Execution
        pipeline = Pipeline(
            reader=reader_manager,
            engine=engine,
            writer=writer_manager,
        )
        pipeline._refine()

        # Assertions
        # Assert read
        reader.read.assert_any_call(table_name="cleaned_table1")
        reader.read.assert_any_call(table_name="cleaned_table2")
        assert reader.read.call_count == 2

        # Assert process
        engine.process.assert_any_call(df_cleaned_1)
        engine.process.assert_any_call(df_cleaned_2)
        assert engine.process.call_count == 2

        # Assert union
        engine.set_refinement_type.assert_called_with(RefinementType.SUMMARY)
        engine.union_dataframes.assert_called_once_with(dataframes=[df_processed_1, df_processed_2])

        # Assert write
        writer.write.assert_called_once_with(dataframe=df_refined, table_name=RefinementType.SUMMARY.value)

    def test_execute_as_extraction(self):
        # Preparation
        extraction_pipeline = Pipeline(
            reader=IOManager(layer=Layer.DATABASE, format=Format.JDBC),
            engine=ExtractionEngine(),
            writer=IOManager(layer=Layer.BRONZE, format=Format.PARQUET),
        )

        # Execution
        with patch("src.etl.core.pipeline.Pipeline._extract", autospec=True) as mock_pipeline_extraction:
            extraction_pipeline.execute(table_to_read="element_entries", table_to_write="entries")

        # Assertion
        mock_pipeline_extraction.assert_called_once_with(extraction_pipeline, table_to_read="element_entries", table_to_write="entries")

    def test_execute_as_cleaning(self):
        # Preparation
        cleaning_pipeline = Pipeline(
            reader=IOManager(layer=Layer.BRONZE, format=Format.PARQUET),
            engine=CleaningEngine(),
            writer=IOManager(layer=Layer.SILVER, format=Format.DELTA),
        )

        # Execution
        with patch("src.etl.core.pipeline.Pipeline._clean", autospec=True) as mock_pipeline_clean:
            cleaning_pipeline.execute(table_to_read="entries")

        # Assertion
        mock_pipeline_clean.assert_called_once_with(cleaning_pipeline, table_to_read="entries")

    def test_execute_as_refinement(self):
        # Preparation
        refinement_pipeline = Pipeline(
            reader=IOManager(layer=Layer.SILVER, format=Format.DELTA),
            engine=RefinementEngine(),
            writer=IOManager(layer=Layer.GOLD, format=Format.DELTA),
        )

        # Execution
        with patch("src.etl.core.pipeline.Pipeline._refine", autospec=True) as mock_pipeline_refine:
            refinement_pipeline.execute()

        # Assertion
        mock_pipeline_refine.assert_called_once_with(refinement_pipeline)


if __name__ == "__main__":
    unittest.main()
