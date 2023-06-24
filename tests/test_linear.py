import unittest
from src.linear import make_linear_call

class TestMakeLinearCall(unittest.TestCase):

	def test_make_linear_call(self):
		self.assertEqual(make_linear_call(12), 4)

unittest.main()