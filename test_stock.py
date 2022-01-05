import unittest
from stock import StockTrade, Stock
from custom_exception import StockNotFoundException
class TestStockTrade(unittest.TestCase):
    def setUp(self):

        self.obj = StockTrade()
        self.stock_obj = Stock('SAM','Common',13,None,250)
        self.obj.data.stocks[self.stock_obj.stock_id] = self.stock_obj
        return super().setUp()

    def test_record_trade_success(self):
        self.obj.record_trade(self.stock_obj.stock_id, 10, 'B', 125)

        trade_record = self.obj.data.get_trade_record(self.stock_obj.stock_id)
        self.assertIsInstance(trade_record, list)
        self.assertEqual(len(trade_record),1)
        self.assertEqual(trade_record[0]['quantity'], 10)

    def test_record_trade_failure(self):
        with self.assertRaises (StockNotFoundException) as exp:
            self.obj.record_trade('PAM', 10, 'B', 125)

            self.assertEqual(exp, "Stock PAM not found")


if __name__ == "__main__":
    unittest.main()
