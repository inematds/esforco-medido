import datetime as dt, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import calendario as c


class Basico(unittest.TestCase):
    def test_pascoa_2026(self):
        self.assertEqual(c.pascoa(2026), dt.date(2026, 4, 5))

    def test_natal_nao_util(self):
        self.assertFalse(c.eh_dia_util(dt.date(2026, 12, 25)))

    def test_sexta_mais_um(self):
        self.assertEqual(c.somar_dias_uteis(dt.date(2026, 11, 13), 1), dt.date(2026, 11, 16))


if __name__ == "__main__":
    unittest.main()
