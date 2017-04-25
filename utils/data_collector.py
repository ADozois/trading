import pandas_datareader as web
import datetime as dt


class DataCollector:
    def __init__(self, name, source, start=None, end=None):
        self.Name = name
        self.Source = source
        self.Last_Fetch = []
        self.Range = [start, end]

    @property
    def last_update(self):
        return self.Last_Fetch

    @last_update.setter
    def last_update(self, value):
        if len(value) == 3:
            self.Last_Fetch = value

    @property
    def source(self):
        return self.Source

    @source.setter
    def source(self, value):
        self.Source = value

    @property
    def name(self):
        return self.Name

    @name.setter
    def name(self, value):
        self.Name = value

    @property
    def range(self):
        return self.Range

    @range.setter
    def range(self, value):
        self.Range = value

    def fetch_data(self):
        data = web.DataReader(self.Name, self.Source, self.get_start_time(), self.get_end_time())
        if not self.Range[0]:
            self.Range[0] = [2010, 1, 1]
        if not self.Range[1]:
            today = dt.date.today()
            self.Range[1] = [today.year, today.month, today.day]
        return data

    def update_data(self):
        today = dt.date.today()
        today = [today.year, today.month, today.day]
        if today != self.Range[1]:
            start = [self.Range[1][0], self.Range[1][1], self.Range[1][2]+1]
            data = web.DataReader(self.Name, self.Source, self.transform_to_datetime(start), self.transform_to_datetime(today))
            self.Range[1] = today
            return data
        else:
            return None

    def get_start_time(self):
        if self.Range[0]:
            return dt.datetime(self.Range[0][0], self.Range[0][1], self.Range[0][2])
        else:
            return None

    def get_end_time(self):
        if self.Range[1]:
            return dt.datetime(self.Range[1][0], self.Range[1][1], self.Range[1][2])
        else:
            return None

    @staticmethod
    def transform_to_datetime(time):
        if time:
            return dt.datetime(time[0], time[1], time[2])
        else:
            return None


class DataCollectorFactory:
    @staticmethod
    def create_data_collector(name, start=None, end=None, source='yahoo'):
        return DataCollector(name, source, start, end)
