"""
Investment portfolio represented as one of Digital Double's Things.


@author: Stanislav Ermokhin
@GitHub: https://github.com/FunnyRabbitIsAHabbit
"""


class Portfolio:
    """
    Block for portfolio properties.
    Data as to be exported from Yahoo!Finance Portfolio 2.0, that is:

    Symbol,Current Price,
    Date,Time,Change,
    Open,High,Low,
    Volume,Trade Date,Purchase Price,
    Quantity,Commission,High Limit,
    Low Limit,Comment.

    """

    def __init__(self):
        pass

    def load_data(self):

        # Simulate csv download from source (Yahoo!Finance)???

        return

    @property
    def current_data(self):

        return

    @property
    def default_currency(self):

        return "USD"

    @property
    def current_cash_holdings(self):

        # Extract from self.load_data returned value

        return
