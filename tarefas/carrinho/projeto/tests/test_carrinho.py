import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from carrinho import total


class Carrinho(unittest.TestCase):
    def test_sem_cupom(self):
        self.assertEqual(total([(50.0, 2)]), 125.0)

    def test_cupom_nao_desconta_frete(self):
        self.assertEqual(total([(100.0, 1)], "DEZ"), 115.0)


if __name__ == "__main__":
    unittest.main()
