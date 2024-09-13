# import logging
# import unittest

# from src.shared.logging.custom_formatter import CustomColoredFormatter


# class TestCustomFormatter(unittest.TestCase):

#     def setUp(self):
#         self.formatter = CustomColoredFormatter(fmt="%(levelname)s - %(message)s")
#         self.record = logging.LogRecord(
#             name="test",
#             level=logging.INFO,
#             pathname="src/module/file.py",
#             lineno=10,
#             msg="Test message",
#             args=(),
#             exc_info=None,
#         )

#     def test_init(self):
#         self.assertEqual(self.formatter.class_name, "TestClass")

#     def test_set_class_name(self):
#         self.formatter.set_class_name("NewClassName")
#         self.assertEqual(self.formatter.class_name, "NewClassName")

#     def test_format_with_src_path(self):
#         formatted_message = self.formatter.format(self.record)
#         self.assertIn("src/module/file.py", self.record.pathname)
#         self.assertIn("TestClass", self.record.funcName)
#         self.assertIn("INFO - Test message", formatted_message)

#     def test_format_without_src_path(self):
#         self.record.pathname = "module/file.py"
#         formatted_message = self.formatter.format(self.record)
#         self.assertEqual(self.record.pathname, "module/file.py")
#         self.assertIn("TestClass", self.record.funcName)
#         self.assertIn("INFO - Test message", formatted_message)


# if __name__ == "__main__":
#     unittest.main()
