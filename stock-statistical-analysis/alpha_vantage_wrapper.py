import pandas as pd
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.timeseries import TimeSeries

class AlphaVantage:

    def get_intraday(self,company="AAPL",timegap="60min"):
        ts = TimeSeries(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        return ts.get_intraday(symbol=company,interval=timegap)

    def get_daily(self,company="AAPL"):
        ts = TimeSeries(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        return ts.get_daily(symbol=company)

    def get_weekly(self,company="AAPL"):
        ts = TimeSeries(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        return ts.get_weekly(symbol=company)

    def get_monthly(self,company="AAPL"):
        ts = TimeSeries(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        return ts.get_monthly(symbol=company)

    def get_sector_intraday(self):
        sp = SectorPerformances(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        data, meta_data = sp.get_sector()
        realtime = data['Rank A: Real-Time Performance']
        return realtime.get('Information Technology'), meta_data

    def get_sector_daily(self):
        sp = SectorPerformances(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        data, meta_data = sp.get_sector()
        day = data['Rank B: Day Performance']
        return day.get('Information Technology'), meta_data

    def get_sector_weekly(self):
        sp = SectorPerformances(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        data, meta_data = sp.get_sector()
        week = data['Rank C: Day Performance']
        return week.get('Information Technology'), meta_data

    def get_sector_monthly(self):
        sp = SectorPerformances(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        data, meta_data = sp.get_sector()
        month = data['Rank D: Month Performance']
        return month.get('Information Technology'), meta_data

    def create_dictionary_of_prices(time_interval):
        sectors = {}
        if time_interval == 'hour':
            sectors['APPLE'] = get_intraday('AAPL')
            sectors['FACEBOOK'] = get_intraday('FB')
            sectors['TECHNOLOGY'] = get_sector_intraday()
        elif time_interval == 'day':
            sectors['APPLE'] = get_daily('APPL')
            sectors['FACEBOOK'] = get_daily('FB')
            sectors['TECHNOLOGY'] = get_sector_daily()
        elif time_interval = 'week':
            sectors['APPLE'] = get_weekly('APPL')
            sectors['FACEBOOK'] = get_weekly('FB')
            sectors['TECHNOLOGY'] = get_sector_weekly()
        elif time_interval = 'month':
            sectors['APPLE'] =  get_monthly('APPL')
            sectors['FACEBOOK'] = get_monthly('FB')
            sectors['TECHNOLOGY'] = get_sector_monthly()
        return sectors
