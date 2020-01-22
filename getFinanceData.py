import pandas as pd
import pandas_datareader as dr
from datetime import datetime, timedelta

class financeData:
    """
      getYahooData fetches real-time Yahoo! finance data(historical data)
      through Yahoo! API and returns a single set of entry used for testing
      -------------
      input:
        keyword
        start_date
      -------------
      output:
         historical data: open price, close price, high price, low price, volumes
      -------------
      citation:
        https://pypi.org/project/fix-yahoo-finance/

    """
    def getYahooData(self, keyword, start_date):
        # start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        print(start_date)
        # print(end_date)
        df = dr.data.get_data_yahoo(keyword, start= start_date, end=start_date)
        print(df.head(1))
        return df.head(1)
        #historical_data = yahoo.get_historical(start_date, end_date)
        #return historical_data
