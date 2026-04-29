import unittest
from common.r3 import R3
from shadow.polyedr import Edge, Facet
import math


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
            Edge(R3(1.1, 0.0, 0.0), R3(1.1, 0.0, 0.0)),  # центр 1.1
            Edge(R3(2.5, 0.0, 0.0), R3(2.5, 0.0, 0.0)),  # центр 2.5
            Edge(R3(1.5, 0.0, 0.0), R3(2.5, 0.0, 0.0)),  # центр 2.0
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

    def test_simple_invisible_edge(self):
        """Одна грань затеняет одно ребро"""
        # Создаём грань (квадрат на уровне z=0)
        facet = Facet([
            R3(0.0, -1.0, 0.0),
            R3(4.0, -1.0, 0.0),
            R3(4.0, 1.0, 0.0),
            R3(0.0, 1.0, 0.0)
        ])

        # Ребро под гранью, полностью невидимое
        # X от 1.5 до 2.5 → центр 2.0 (подходит)
        # Y от -0.5 до 0.5, Z = -1
        edge = Edge(R3(1.5, -0.5, -1.0), R3(2.5, 0.5, -1.0))
        edge.shadow(facet)
        self.assertTrue(edge.if_fully_invisible())
        self.assertAlmostEqual(edge.proj_x(), 2.0)

        expected_len = math.sqrt(2.0)
        self.assertAlmostEqual(edge.proj_len(), expected_len)
        self.assertLess(abs(edge.proj_x() - 2.0), 1.0)
        total = edge.proj_len() if abs(edge.proj_x() - 2.0) < 1.0 else 0.0
        self.assertAlmostEqual(total, expected_len)

    def test_two_invisible_edges_one_visible(self):
        """Два невидимых ребра (одно подходит, другое нет) + одно видимое"""

        # Грань-затенение
        facet = Facet([
            R3(0.0, -2.0, 0.0),
            R3(5.0, -2.0, 0.0),
            R3(5.0, 2.0, 0.0),
            R3(0.0, 2.0, 0.0)
        ])

        # Ребро 1: полностью невидимое
        edge1 = Edge(R3(1.0, -1.0, -1.0), R3(3.0, 1.0, -1.0))

        # Ребро 2: полностью невидимое
        edge2 = Edge(R3(3.5, -1.0, -1.0), R3(4.5, 1.0, -1.0))

        # Ребро 3: видимое
        edge3 = Edge(R3(1.5, -0.5, 1.0), R3(3.5, 0.5, 1.0))

        for e in [edge1, edge2, edge3]:
            e.shadow(facet)

        self.assertTrue(edge1.if_fully_invisible())
        self.assertTrue(edge2.if_fully_invisible())
        self.assertFalse(edge3.if_fully_invisible())

        self.assertAlmostEqual(edge1.proj_x(), 2.0)
        self.assertAlmostEqual(edge2.proj_x(), 4.0)

        total = 0.0
        if edge1.if_fully_invisible() and abs(edge1.proj_x() - 2.0) < 1.0:
            total += edge1.proj_len()
        if edge2.if_fully_invisible() and abs(edge2.proj_x() - 2.0) < 1.0:
            total += edge2.proj_len()
        if edge3.if_fully_invisible() and abs(edge3.proj_x() - 2.0) < 1.0:
            total += edge3.proj_len()

        expected_length = math.sqrt(8.0)
        self.assertAlmostEqual(total, expected_length)

