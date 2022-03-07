import time
import datetime
import math
from decimal import Decimal

class Stock:
    def __init__(self, name):
        self.name = name

    def price(self, date):
        return self.get_dummy_price(date)
    
    def get_dummy_price(self, date):
        """
        Generate a deterministic value from the date(in timestamp)
        and stock name(sum unicode points of every character),
        this value become to decimal and it's returned as a dummy price
        """
        from_name = sum([ord(c) for c in self.name])
        from_date = time.mktime(date.timetuple())
        combine = str(from_name * from_date) 
        price = int(combine[5:10]) / 100
        return Decimal(str(price))

class Portfolio:
    def __init__(self, stocks):
        self.stocks = stocks

    # this function can be an util
    def get_years(self, from_date, to_date):
        """
        In case if is necessary consider a leap year,
        we can use calendar lib to know if the year is
        a leap year, and update day_in_year variable
        """
        delta = to_date - from_date
        day_in_years = 0.002738
        years = Decimal(math.ceil((delta.days * day_in_years) * 100.0) /  100.0)
        return years

    def profit(self, from_date, to_date):
        initial_value = sum([stock.price(from_date) for stock in self.stocks])
        final_value = sum([stock.price(to_date) for stock in self.stocks])
        return (final_value - initial_value) / initial_value

    def annualized_profit(self, from_date, to_date):
        return_rate = self.profit(from_date, to_date)
        years = self.get_years(from_date, to_date)
        profit = ((1 + return_rate) ** (1 / years)) - 1
        return round(profit, 2)

if __name__ == "__main__":
    portfolio = Portfolio([Stock("AMZ"), Stock("GOOGL"), Stock("TSLA")])
    from_date = datetime.datetime.strptime("20/06/2020", "%d/%m/%Y")
    to_date = datetime.datetime.strptime("20/12/2020", "%d/%m/%Y")
    print(portfolio.annualized_profit(from_date, to_date))
