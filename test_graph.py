import unittest
import graph as g

class TestGraph(unittest.TestCase):

	def test_create_graph(self):
		G = g.create_graph()
		self.assertEqual(len(G.nodes()) ,0)

		
if __name__ == '__main__':
	unittest.main()