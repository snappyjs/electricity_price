from datetime import datetime
from src.service.http_el_price_service import ElprisetJustNuService
import unittest


class TestHttpElPriceService(unittest.TestCase):
    def test_get_price(self):
        service = ElprisetJustNuService()
        price = service.get_price(datetime(2024, 11, 8, 12, 00, 00), "SE3")
        self.assertIsNotNone(price)
        self.assertEqual(0.48443, price, "Price is not correct")


if __name__ == "__main__":
    unittest.main()
