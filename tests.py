import datetime
import unittest
from unittest import mock
from decimal import Decimal
from portfolio import Stock, Portfolio

class TestStock(unittest.TestCase):
    def test_random_price_is_deterministic(self):
        amz = Stock("amz")
        date = datetime.datetime.strptime("20/06/2020", "%d/%m/%Y")
        random_price_1 = amz.get_dummy_price(date)
        random_price_2 = amz.get_dummy_price(date)
        assert random_price_2 == random_price_1

        date = datetime.datetime.strptime("20/06/2021", "%d/%m/%Y")
        random_price_3 = amz.get_dummy_price(date)
        assert random_price_1 != random_price_3
    
    def test_get_price(self):
        with mock.patch.object(Stock, "get_dummy_price") as get_dummy_price_mock:
            results = [12]
            get_dummy_price_mock.side_effect = results
            amz = Stock("amz")
            date = datetime.datetime.strptime("20/06/2020", "%d/%m/%Y")
            price = amz.price(date)

            assert price == 12

class TestPortfolio(unittest.TestCase):
    def test_get_years(self):
        portfolio = Portfolio([Stock("AMZ"), Stock("GOOGL"), Stock("TSLA")])
        from_date = datetime.datetime.strptime("20/06/2020", "%d/%m/%Y")
        to_date = datetime.datetime.strptime("20/06/2021", "%d/%m/%Y")
        years = portfolio.get_years(from_date, to_date)
        assert years == 1
    
    def test_profit(self):
        with mock.patch.object(Stock, "get_dummy_price") as get_dummy_price_mock:
            results = [Decimal(12), Decimal(15), Decimal(20), Decimal(40), Decimal(60), Decimal(30)]
            get_dummy_price_mock.side_effect = results
            portfolio = Portfolio([Stock("AMZ"), Stock("GOOGL"), Stock("TSLA")])
            from_date = datetime.datetime.strptime("20/06/2020", "%d/%m/%Y")
            to_date = datetime.datetime.strptime("20/12/2020", "%d/%m/%Y")

            # ((12 + 15 + 20) - (40 + 60 + 30)) / 47 = 1.7659574468085106...
            expected_value = (sum(results[3:]) - sum(results[:3])) / 47
            profit = portfolio.profit(from_date, to_date)
            assert profit == expected_value
        
    def test_annualized_profit(self):
        with mock.patch.object(Stock, "get_dummy_price") as get_dummy_price_mock:
            results = [Decimal(1000), Decimal(500), Decimal(500), Decimal(3000), Decimal(1000), Decimal(1000)]
            get_dummy_price_mock.side_effect = results
            portfolio = Portfolio([Stock("AMZ"), Stock("GOOGL"), Stock("TSLA")])
            from_date = datetime.datetime.strptime("20/06/2020", "%d/%m/%Y")
            to_date = datetime.datetime.strptime("20/06/2025", "%d/%m/%Y")
            annualized_profit = portfolio.annualized_profit(from_date, to_date)
            """
            return value = ((3000 + 1000 + 1000) - (1000 + 500 + 500)) / 2000 = 1.5
            profit = ((1 + 1.5) ** (1 / 5)) - 1
            """
            expected_profit = round(Decimal(0.20), 2)
            assert annualized_profit == round(expected_profit, 2)

if __name__ == '__main__':
    unittest.main()