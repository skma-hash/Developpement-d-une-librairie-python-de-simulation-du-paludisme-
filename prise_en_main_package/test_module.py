import unittest

from prise_en_main_package.Module1 import triple, perimetre 
class TestModule(unittest.TestCase):
    def test_triple(self):
        self.assertEqual 