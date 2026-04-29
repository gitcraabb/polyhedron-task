import unittest
from common.r3 import R3
from shadow.polyedr import Edge, Facet


class TestInvisibleEdgesSum(unittest.TestCase):

    def test_proj_x(self):
        e = Edge(R3(1.0, 0.0, 0.0), R3(3.0, 0.0, 0.0))
        self.assertEqual(e.proj_x(), 2.0)

        e = Edge(R3(0.0, 0.0, 0.0), R3(2.0, 0.0, 0.0))
        self.assertEqual(e.proj_x(), 1.0)

    def test_proj_len(self):
        e = Edge(R3(0.0, 0.0, 0.0), R3(3.0, 4.0, 0.0))
        # sqrt((3-0)² + (4-0)²) = 5
        self.assertAlmostEqual(e.proj_len(), 5.0)

        e = Edge(R3(0.0, 0.0, 5.0), R3(0.0, 0.0, 10.0))
        self.assertAlmostEqual(e.proj_len(), 0.0)

    def test_dist(self):
        should_include = [
            Edge(R3(1.1, 0.0, 0.0), R3(1.1, 0.0, 0.0)),  #1.1
            Edge(R3(2.5, 0.0, 0.0), R3(2.5, 0.0, 0.0)),  #2.5
            Edge(R3(1.5, 0.0, 0.0), R3(2.5, 0.0, 0.0)),  #2.0
        ]

        should_exclude = [
            Edge(R3(0.5, 0.0, 0.0), R3(0.5, 0.0, 0.0)),  # центр 0.5, расстояние 1.5
            Edge(R3(3.1, 0.0, 0.0), R3(3.1, 0.0, 0.0)),  # центр 3.1, расстояние 1.1
            Edge(R3(0.0, 0.0, 0.0), R3(1.0, 0.0, 0.0)),  # центр 0.5
            Edge(R3(3.0, 0.0, 0.0), R3(5.0, 0.0, 0.0)),  # центр 4.0
        ]

        for e in should_include:
            self.assertLess(abs(e.proj_x() - 2.0), 1.0)

        for e in should_exclude:
            self.assertGreaterEqual(abs(e.proj_x() - 2.0), 1.0)
