# from unittest.mock import MagicMock, patch

# import pytest

# from src.etl.orchestrator import orchestrate_etl_process


# @pytest.fixture
# def mock_pipeline():
#     with patch("src.etl.core.pipeline.Pipeline", autospec=True) as mock_pipeline_class:
#         mock_pipeline_instance = MagicMock()
#         mock_pipeline_class.return_value = mock_pipeline_instance
#         yield mock_pipeline_instance


# @pytest.fixture
# def mock_schema_updater():
#     with patch("src.database.schema.updater.DatabaseSchemaUpdater", autospec=True) as mock_updater_class:
#         mock_updater_instance = MagicMock()
#         mock_updater_class.return_value = mock_updater_instance
#         yield mock_updater_instance


# def test_orchestrate_etl_process_with_refresh_schema(mock_pipeline, mock_schema_updater):
#     orchestrate_etl_process(refresh_schema=True)

#     # Check if DatabaseSchemaUpdater is called
#     mock_schema_updater.update_element_schemas.assert_called_once()

#     # Verify pipelines execute expected calls
#     assert mock_pipeline.execute.call_count == 4
#     mock_pipeline.execute.assert_any_call(table_to_read="element_entries", table_to_write="entries")
#     mock_pipeline.execute.assert_any_call(table_to_read="element_schemas", table_to_write="schemas")
#     mock_pipeline.execute.assert_any_call(table_to_read="entries")
#     mock_pipeline.execute.assert_any_call()


# def test_orchestrate_etl_process_without_refresh_schema(mock_pipeline, mock_schema_updater):
#     orchestrate_etl_process(refresh_schema=False)

#     # Ensure DatabaseSchemaUpdater is not called
#     mock_schema_updater.update_element_schemas.assert_not_called()

#     # Verify pipelines execute expected calls
#     assert mock_pipeline.execute.call_count == 4
#     mock_pipeline.execute.assert_any_call(table_to_read="element_entries", table_to_write="entries")
#     mock_pipeline.execute.assert_any_call(table_to_read="element_schemas", table_to_write="schemas")
#     mock_pipeline.execute.assert_any_call(table_to_read="entries")
#     mock_pipeline.execute.assert_any_call()
