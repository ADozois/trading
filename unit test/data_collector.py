import unittest
from utils.data_collector import DataCollectorFactory
import datetime as dt
import pandas_datareader.data as web
import pandas.util.testing as pdt


class TestDataCollector(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_collector_1 = DataCollectorFactory.create_data_collector('TSLA', None, None, source='yahoo')
        self.data_collector_2 = DataCollectorFactory.create_data_collector('TSLA', [2016, 1, 1], [2016, 1, 25],
                                                                           source='yahoo')
        self.data_1 = self.data_collector_1.fetch_data()
        self.data_2 = self.data_collector_2.fetch_data()

    def test_range_none(self):
        today = dt.date.today()
        self.assertEqual(self.data_collector_1.range, [[2010, 1, 1], [today.year, today.month, today.day]])

    def test_name_setter(self):
        self.data_collector_1.name = 'GOOGL'
        self.assertEqual(self.data_collector_1.name, 'GOOGL')

    def test_start_end_time(self):
        self.assertEqual(self.data_collector_2.get_start_time(), dt.datetime(2016, 1, 1))
        self.assertEqual(self.data_collector_2.get_end_time(), dt.datetime(2016, 1, 25))

    def test_update_function(self):
        today = dt.date.today()
        base = web.DataReader('TSLA', 'yahoo', dt.datetime(2017, 1, 6), dt.datetime(today.year, today.month, today.day))
        test_upd_1 = DataCollectorFactory.create_data_collector('TSLA', [2017, 1, 1], [2017, 1, 5], source='yahoo')
        new_data = test_upd_1.update_data()
        pdt.assert_frame_equal(base, new_data)


if __name__ == '__main__':
    unittest.main()
