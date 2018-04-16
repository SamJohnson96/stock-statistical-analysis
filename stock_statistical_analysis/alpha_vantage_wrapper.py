import pandas as pd
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.timeseries import TimeSeries
import signal

class TimedOut(Exception):
  pass

class AlphaVantage:

    ts = TimeSeries(key='QL2Z176B6Q3JYM6A', output_format='pandas')
    sp = SectorPerformances(key='QL2Z176B6Q3JYM6A', output_format='pandas')

    def deadline(timeout, *args):
      def decorate(f):
        def handler(signum, frame):
          raise TimedOut()

        def new_f(*args):
          signal.signal(signal.SIGALRM, handler)
          signal.alarm(timeout)
          return f(*args)
          signa.alarm(0)

        new_f.__name__ = f.__name__
        return new_f
      return decorate


    def get_intraday(self,company="AAPL",timegap="60min"):
        """Calls AlphaVantages API and gets the intraday figures for the given company.
        Args:
            company (string): Company name that we will look for
            timegap (string): The time interval we look at during the day
        Returns:
            Panda Dataframe: Dataframe of stock information for the given request

        """
        print('entered method')
        data, meta_data = self.ts.get_intraday(symbol=company,interval=timegap)
        return data

    def get_days_information(self,company="AAPL"):
        """Calls AlphaVantages API and gets the days figures for the given company.
        Args:
            company (string): Company name that we will look for
        Returns:
            Panda Dataframe: Dataframe of stock information for the given request

        """
        data, meta_data = self.ts.get_daily(symbol=str(company))
        return data

    def get_weekly_information(self,company="AAPL"):
        """Calls AlphaVantages API and gets the weeks figures for the given company.
        Args:
            company (string): Company name that we will look for
        Returns:
            Panda Dataframe: Dataframe of stock information for the given request
        """
        data, meta_data = self.ts.get_weekly(symbol=str(company))
        return data

    def get_monthly_information(self,company="AAPL"):
        """Calls AlphaVantages API and gets the months figures for the given company.
        Args:
            company (string): Company name that we will look for
        Returns:
            Panda Dataframe: Dataframe of stock information for the given request

        """
        data, meta_data = self.ts.get_monthly(symbol=str(company))
        return data

    def get_sector_intraday(self):
        sp = SectorPerformances(key='QL2Z176B6Q3JYM6A', output_format='pandas')
        data, meta_data = self.sp.get_sector()
        realtime = data['Rank A: Real-Time Performance']
        return realtime.get('Information Technology')

    def get_sector_daily(self):
        data, meta_data = self.sp.get_sector()
        day = data['Rank B: Day Performance']
        return day.get('Information Technology')

    def get_sector_weekly(self):
        data, meta_data = self.sp.get_sector()
        week = data['Rank C: Day Performance']
        return week.get('Information Technology')

    def get_sector_monthly(self):
        data, meta_data = self.sp.get_sector()
        month = data['Rank D: Month Performance']
        return month.get('Information Technology')

    @deadline(20)
    def create_dictionary_of_prices(self,time_interval):
        """Creates a dictionary of stock prices for the given time interval using the classes methods API.
        Args:
            time_interval (string): The time interval we will be looking for /HOUR/DAY/WEEK/MONTH
        Returns:
            Dictionary: entries 'apple','facebook','technology'
        """
        sectors = {}
        if time_interval == 'hour':
            sectors['apple'] = self.get_intraday(company='AAPL')
            sectors['facebook'] = self.get_intraday(company='FB')
            sectors['technology'] = self.get_sector_intraday()
        elif time_interval == 'day':
            sectors['apple'] = self.get_days_information(company='AAPL')
            sectors['facebook'] = self.get_days_information(company='FB')
            sectors['technology'] = self.get_sector_daily()
        elif time_interval == 'week':
            sectors['apple'] = self.get_weekly_information(company='AAPL')
            sectors['facebook'] = self.get_weekly_information(company='FB')
            sectors['technology'] = self.get_sector_weekly()
        elif time_interval == 'month':
            sectors['apple'] =  self.get_monthly_information('AAPL')
            sectors['facebook'] = self.get_monthly_information('FB')
            sectors['technology'] = self.get_sector_monthly()

        return sectors
