
from datetime import datetime, timedelta

from custom_exception import StockNotFoundException, TradeTypeException

class StockExchangeData:
    """
    Stock Exchange class to hold all stock exchange transactions
    """
    #variable to hold all stock in the excahnge
    stocks = {}

    #variable to hold all stock trading info
    stock_trade_data = {}

    @classmethod
    def add_stock(cls,stock):
        """
        Add a stock to exchange

        Parameters
        ----------
        stock: Stock
            object of Stock class

        Returns
        -------
        None
        """
        cls.stocks.update({stock.stock_id: stock})

    @classmethod
    def get_stock(cls, stock_symbol):
        """
        Get a stock detail from the exchange

        Parameters
        ----------
        stock: str
            3 letter stock symbol/stock_id

        Returns
        -------
        Stock
            Return an object of class Stock
        """
        return cls.stocks.get(stock_symbol)

    @classmethod
    def get_all_stocks(cls):
        """
        Get all stock detail in the exchange

        Parameters
        ----------

        Returns
        -------
        dict
        Returns a dict with all stocks available in the exchange
        """
        return cls.stocks

    @classmethod
    def record_trade(cls, stock_symbol, quantity, trade_type, price, timestamp):
        """
        Record a trade

        Parameters
        ----------
        stock_symbol: str
            3 letter identifier for the stock
        quantity: int
            Stock trade quantity
        trade_type: str
            Stock trade type (BUY/SELL)
        price: float
            Stock trade price
        timestamp: datetime
            Trade transaction time

        Returns
        -------

        """

        if not (stock_symbol in cls.stock_trade_data):
            cls.stock_trade_data[stock_symbol] = []

        cls.stock_trade_data[stock_symbol].append({'quantity': quantity, 'type': trade_type, 'price': price, 'timestamp': timestamp})

    @classmethod
    def get_trade_record(cls, stock_symbol):
        """
        Get a trade record for the given stock

        Parameters
        ----------
        stock_symbol: str
            3 letter stock symbol/stock_id

        Returns
        -------
        List
            Return a list of trade details dictionary
        """
        return cls.stock_trade_data.get(stock_symbol, [])

    @classmethod
    def get_all_trade_records(cls):
        """
        Get all trade records

        Parameters
        ----------

        Returns
        -------
        Dict
            Return a dict of trade details
        """
        return cls.stock_trade_data


class Stock:

    """
    The Stock class
    """

    def __init__(self, stock_symbol, stock_type, last_divident, fixed_divident, par_value):
        self._stock_symbol = stock_symbol
        self.stock_type = stock_type
        self.last_divident = last_divident
        self.fixed_divident = fixed_divident
        self.par_value = par_value
    
    #getter
    @property
    def stock_id(self):
        return self._stock_symbol

    #setter
    @stock_id.setter
    def stock_id(self, stock_id):
        self._stock_symbol = stock_id

class StockCalculations:

    """
    A Class to handle all stock calculations
    """

    def __init__(self):
        #Since the problem statement doesn't require a static storage, the date is stored accessed form StockExchangeData class 
        self.data = StockExchangeData

    def get_divident_yield(self, stock_id, price):
        """
        Calculate divident yield

        Parameters
        ----------
        stock_id: str
            3 letter identifier for the stock
        price: float
            Stock trade price

        Returns
        -------
        float
            Calculated divident yield
        """
        stock = self.data.get_stock(stock_id)

        if not stock:
            return None

        if stock.stock_type.upper() == 'COMMON':
            return stock.last_divident / price

        elif stock.stock_type.upper() == 'PREFERRED':
            return ( stock.fixed_divident * stock.par_value ) / price

    def get_pe_ratio(self, stock_id, price):
        """
        Calculate P/E Ratio

        Parameters
        ----------
        stock_id: str
            3 letter identifier for the stock
        price: float
            Stock trade price

        Returns
        -------
        float
            Calculated p/e ratio value
        """
        stock = self.data.get_stock(stock_id)

        if not stock:
            return None
        
        divident = self.get_divident_yield(stock_id, price)
        return price / divident

    def volume_weighted_price(self, stock_id, time_period=5):
        """
        Calculate volume weighted price

        Parameters
        ----------
        stock_id: str
            3 letter identifier for the stock
        time_period: int optional default=5
            time perion in minutes

        Returns
        -------
        float
            Calculated volume weighted price
        """
        trades = self.data.get_trade_record(stock_id)

        current_time = datetime.now()

        time_window = current_time - timedelta(minutes=time_period)

        quantity = 0
        price_quantity = 0
        count = 0

        for item in trades [::-1]:
            if time_period and time_window >= item['timestamp']:
                break
            
            quantity +=  item['quantity']
            price_quantity +=  ( item['price'] * item['quantity'] )
            count += 1
            
        if count and quantity:
            return price_quantity / quantity
        else:
            return None

    def GBCE(self):

        """
        Calculate GBCE of all share index using geometric mean

        Parameters
        ----------

        Returns
        -------
        float
            Calculated geometric mean
        """
        trade_record = self.data.get_all_trade_records()

        total_volume_weight = 1
        stock_count = 0

        for trade in trade_record:
            volume_weight = self.volume_weighted_price(trade, 0)
            if volume_weight:
                total_volume_weight *= volume_weight
                stock_count += 1

        geometric_mean = total_volume_weight ** (1 / stock_count)

        return geometric_mean


class StockTrade:
    """
    A Class used to handle stock tradings
    """
    def __init__(self):
        self.data = StockExchangeData

    def record_trade(self, stock_id, quantity, trade_type, price):

        """
        Record a trade

        Parameters
        ----------
        stock_id: str
            3 letter identifier for the stock
        quantity: int
            Stock trade quantity
        trade_type: str
            Stock trade type (BUY/SELL)
        price: float
            Stock trade price

        Returns
        -------
        bool
            True or False based on the transaction status
        """

        stock = self.data.get_stock(stock_id)

        if not stock:
            raise StockNotFoundException(f"Stock {stock_id} not found")

        if trade_type.upper() not in ('B','S'):
            raise TradeTypeException(f"Trade type {trade_type} is not valid")

        self.data.record_trade(stock_id, quantity, trade_type, price, datetime.now())
        


