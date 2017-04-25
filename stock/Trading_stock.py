import pickle

TMX_FILENAME = 'data/tsx_stock_list.pickle'


class TradingStock:
    def __init__(self):
        self.trading_stocks_names = self.load_stock_list(TMX_FILENAME)
        self.trading_stocks = []

    @staticmethod
    def load_stock_list(file_name):
        with open(file_name, 'rb') as f:
            stocks = pickle.load(f)
        return stocks

    def save_stock_list(self, file_name=None):
        if file_name:
            with open(file_name, 'wb') as f:
                pickle.dump(self.trading_stocks_names, f)
        else:
            with open(TMX_FILENAME, 'wb') as f:
                pickle.dump(self.trading_stocks_names, f)

    def update(self):
        for stock in self.trading_stocks:
            stock.update_stock()