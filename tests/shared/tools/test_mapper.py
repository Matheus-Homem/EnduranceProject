import unittest
import os
from src.shared.tools.mapper import Mapper

class TestMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = Mapper()

    def test_mapper_in_outputs(self):
        self.assertEqual(self.mapper.outputs.reports(), os.path.join('outputs', 'reports'))

    def test_mapper_in_resources(self):
        self.assertEqual(self.mapper.resources.yaml(), os.path.join('resources', 'yaml'))

    def test_mapper_in_data(self):
        self.assertEqual(self.mapper.data.ingestion(), os.path.join('data', 'ingestion'))
        self.assertEqual(self.mapper.data.cleaned(), os.path.join('data', 'cleaned'))
        self.assertEqual(self.mapper.data.refined(), os.path.join('data', 'refined'))

    def test_mapper_in_src(self):
        self.assertEqual(self.mapper.src.etl(), os.path.join('src', 'etl'))
        self.assertEqual(self.mapper.src.shared(), os.path.join('src', 'shared'))
        self.assertEqual(self.mapper.src.report(), os.path.join('src', 'report'))
        self.assertEqual(self.mapper.src.web(), os.path.join('src', 'web'))

if __name__ == '__main__':
    unittest.main()