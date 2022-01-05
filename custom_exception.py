
class StockNotFoundException(Exception):
    """Exception raised when a stock is not found

    Attributes:
        message: str
            Exception message
    """
    def __init__(self, message="Stock not found"):
        self.message = message
        super().__init__(self.message)

class TradeTypeException(Exception):
    """Exception raised if a trade type is not B or S

    Attributes:
        message: str
            Exception message
    """
    def __init__(self, message="Wrong Trade Type"):
        self.message = message
        super().__init__(self.message)