import abc
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates


class Chart:
    def __init__(self, data):
        __metaclass__ = abc.ABCMeta
        self.data = data
        self.chart = plt

    @abc.abstractmethod
    def show(self):
        """To Show the chart"""

    @abc.abstractmethod
    def create_chart(self):
        """To create the actual chart"""


class CandlestickChart(Chart):
    def __init__(self, data, sampling, range_data=None):
        super(CandlestickChart, self).__init__(data)
        self.candle_data = self.transform_data(self.data, sampling)
        self.range_data = range_data
        self.create_chart()

    @staticmethod
    def transform_data(data, sampling):
        data_ohlc = [None]*2
        data_ohlc[0] = data['Adj Close'].resample(sampling).ohlc()
        data_ohlc[0].reset_index(inplace=True)
        data_ohlc[0]['Date'] = data_ohlc[0]['Date'].map(mdates.date2num)

        data_ohlc[1] = data['Volume'].resample(sampling).sum()
        return data_ohlc

    def create_chart(self):
        ax1 = self.chart.subplot2grid((7, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = self.chart.subplot2grid((7, 1), (6, 0), rowspan=1, colspan=1, sharex=ax1)
        ax1.xaxis_date()

        candlestick_ohlc(ax1, self.candle_data[0].values, width=2, colorup='g')
        ax2.fill_between(self.candle_data[1].index.map(mdates.date2num), self.candle_data[1].values, 0)

    @property
    def range_data(self):
        return self.range_data

    @range_data.setter
    def range_data(self, value):
        if self.__check_range(value):
            self.range_data = value

    def show(self):
        self.chart.show()

    @staticmethod
    def __check_range(range_data):
        if range_data:
            for i in range(0, len(range_data)):
                if not isinstance(range_data[0][i], int) and not isinstance(range_data[1][i], int):
                    return False
            return True
