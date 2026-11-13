import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intervalos import juntar


class Basico(unittest.TestCase):
    def test_sobrepoe(self):
        self.assertEqual(juntar(["09:00-10:30", "10:00-11:00"]), ["09:00-11:00"])

    def test_separados(self):
        self.assertEqual(juntar(["14:00-15:00", "09:00-10:00"]), ["09:00-10:00", "14:00-15:00"])

    def test_vazio(self):
        self.assertEqual(juntar([]), [])


if __name__ == "__main__":
    unittest.main()
