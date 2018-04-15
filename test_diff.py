# Test Diff 

import unittest
import diff


class TestDiff(unittest.TestCase):

	def test_diff_result(self):

		list1 = ['abc','def']
		list2 = ['abc','xyz']
		res = diff.diff_result(list1, list2)
		
		if len(res) < 1:
			self.fail('Result of diff is empty. Diff service failed!')


if __name__ == '__main__':
	unittest.main()