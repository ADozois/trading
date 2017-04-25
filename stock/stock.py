from utils.data_collector import DataCollectorFactory
import datetime as dt


class Stock:
    def __init__(self, name, start=None, end=None, source='yahoo'):
        self.Data_collector = DataCollectorFactory.create_data_collector(name, start, end, source)
        self.Name = name
        self.Last_Open = 0
        self.Last_Close = 0
        self.Data = self.fetch_stock()

    @property
    def last_open(self):
        return self.Last_Open

    @last_open.setter
    def last_open(self, value):
        if value >= 0:
            self.Last_Open = value
        else:
            raise ValueError

    @property
    def last_close(self):
        return self.Last_Close

    @last_close.setter
    def last_close(self, value):
        if value >= 0:
            self.Last_Close = value
        else:
            raise ValueError

    def update_stock(self):
        new_data = self.Data_collector.update_data()
        self.Data.append(new_data)
        self.Last_Close = self.Data['Close'][-1]
        self.Last_Open = self.Data['Open'][-1]

    def fetch_stock(self):
        data = self.Data_collector.fetch_data()
        self.Last_Open = data['Open'][-1]
        self.Last_Close = data['Close'][-1]
        return data

    def get_metric_interval(self, metric, start=None, end=None):
        if not start:
            start = [2010, 1, 1]
        if not end:
            today = dt.date.today()
            end = [today.year, today.month, today.day]

        if metric not in ['Open', 'Close', 'Adj Close', 'Volume', 'High', 'Low']:
            raise ValueError('Value pass to metric is not supported')
        else:
            return self.Data[metric].loc[dt.datetime(start[0], start[1], start[2]):dt.datetime(end[0], end[1], end[2])]

    def get_data_interval(self, start=None, end=None):
        if not start:
            start = [2010, 1, 1]
        if not end:
            today = dt.date.today()
            end = [today.year, today.month, today.day]
        return self.Data.loc[dt.datetime(start[0], start[1], start[2]):dt.datetime(end[0], end[1], end[2])]
