import unittest
from unittest.mock import MagicMock, patch

from src.etl.orchestrator import orchestrate_etl_process


class TestOrchestrateETLProcess(unittest.TestCase):

    @patch("src.etl.orchestrator.Pipeline")
    @patch("src.etl.orchestrator.DatabaseSchemaUpdater")
    def test_orchestrate_etl_process(self, MockDatabaseSchemaUpdater, MockPipeline):
        mock_extraction_pipeline = MagicMock()
        mock_cleaning_pipeline = MagicMock()
        mock_refinement_pipeline = MagicMock()
        mock_schema_updater = MagicMock()

        MockPipeline.side_effect = [mock_extraction_pipeline, mock_cleaning_pipeline, mock_refinement_pipeline]
        MockDatabaseSchemaUpdater.return_value = mock_schema_updater

        orchestrate_etl_process()

        mock_extraction_pipeline.execute.assert_called_once()
        mock_cleaning_pipeline.execute.assert_called_once()
        mock_refinement_pipeline.execute.assert_called_once()
        mock_schema_updater.update_element_schemas.assert_called_once()


if __name__ == "__main__":
    unittest.main()
