# import unittest
# from unittest.mock import MagicMock, patch

# from src.etl.definitions import Layer
# from src.etl.io.database import DatabaseHandler
# from src.etl.ports import DatabaseDF


# class TestDatabaseReader(unittest.TestCase):

#     @patch("database.DatabaseExecutorBuilder")
#     @patch("database.ElementEntries")
#     def test_read(self, MockElementEntries, MockDatabaseExecutorBuilder):
#         mock_executor = MagicMock()
#         mock_entries = MagicMock(spec=DatabaseDF)
#         mock_executor.select.return_value = mock_entries
#         MockDatabaseExecutorBuilder.return_value.__enter__.return_value = mock_executor

#         reader = DatabaseHandler(layer=Layer.DATABASE)

#         result = reader.read()

#         mock_executor.select.assert_called_once_with(MockElementEntries)
#         self.assertEqual(result, mock_entries)

#     def test_write(self):
#         reader = DatabaseHandler(layer=Layer.DATABASE)

#         with self.assertRaises(NotImplementedError):
#             reader.write(None)


# if __name__ == "__main__":
#     unittest.main()
