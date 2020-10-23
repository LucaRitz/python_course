import unittest

import ai.travelling_salesman as tr


class TravellingSalesmanTest(unittest.TestCase):

    def test_travellingSalesman(self):
        # Act
        result = tr.traveller(TravellingSalesmanTest.__city(), 100)

        # Assert
        self.assertIsNotNone(result)

    @staticmethod
    def __city():
        city_a = tr.Node(1)
        city_b = tr.Node(2)
        city_c = tr.Node(3)
        city_d = tr.Node(4)
        city_e = tr.Node(5)
        city_f = tr.Node(6)

        city_a.append_child(city_b, 10)
        city_a.append_child(city_c, 5)
        city_a.append_child(city_d, 7)

        city_b.append_child(city_a, 10)
        city_b.append_child(city_c, 3)
        city_b.append_child(city_d, 9)

        city_c.append_child(city_a, 5)
        city_c.append_child(city_b, 3)
        city_c.append_child(city_d, 2)
        city_c.append_child(city_e, 4)

        city_d.append_child(city_a, 7)
        city_d.append_child(city_b, 9)
        city_d.append_child(city_c, 2)
        city_d.append_child(city_f, 20)

        city_e.append_child(city_c, 4)
        city_e.append_child(city_f, 3)

        city_f.append_child(city_e, 3)
        city_f.append_child(city_d, 20)

        return city_a
