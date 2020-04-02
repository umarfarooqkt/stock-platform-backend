# Quandl for financial analysis, pandas and numpy for data manipulation
# fbprophet for additive models
import quandl
import pandas as pd
import numpy as np
import fbprophet

# Class for analyzing and (attempting) to predict future prices
# Contains a number of visualizations and analysis methods
class Stocker():

    # Initialization requires a ticker symbol
    def __init__(self, ticker, exchange='WIKI'):

        # Enforce capitalization
        ticker = ticker.upper()

        # Symbol is used for labeling plots
        self.symbol = ticker

        # Use Personal Api Key
        quandl.ApiConfig.api_key = 'U-m-xTvejNiPHWNa8SzH'

        # Retrieval the financial data
        try:
            stock = quandl.get('%s/%s' % (exchange, ticker))

        except Exception as e:
            print('Error Retrieving Data.')
            print(e)
            return

        # Set the index to a column called Date
        stock = stock.reset_index(level=0)

        # Columns required for prophet
        stock['ds'] = stock['Date']

        if ('Adj. Close' not in stock.columns):
            stock['Adj. Close'] = stock['Close']
            stock['Adj. Open'] = stock['Open']

        stock['y'] = stock['Adj. Close']
        stock['Daily Change'] = stock['Adj. Close'] - stock['Adj. Open']

        # Data assigned as class attribute
        self.stock = stock.copy()

        # Minimum and maximum date in range
        self.min_date = min(stock['Date'])
        self.max_date = max(stock['Date'])

        # Find max and min prices and dates on which they occurred
        self.max_price = np.max(self.stock['y'])
        self.min_price = np.min(self.stock['y'])

        self.min_price_date = self.stock[self.stock['y'] == self.min_price]['Date']
        self.min_price_date = self.min_price_date[self.min_price_date.index[0]]
        self.max_price_date = self.stock[self.stock['y'] == self.max_price]['Date']
        self.max_price_date = self.max_price_date[self.max_price_date.index[0]]

        # The starting price (starting with the opening price)
        self.starting_price = float(self.stock.loc[0, 'Adj. Open'])

        # The most recent price
        self.most_recent_price = float(self.stock.loc[self.stock.index[-1], 'y'])

        # Whether or not to round dates
        self.round_dates = True

        # Number of years of data to train on
        self.training_years = 3

        # Prophet parameters
        # Default prior from library
        self.changepoint_prior_scale = 0.05
        self.weekly_seasonality = False
        self.daily_seasonality = False
        self.monthly_seasonality = True
        self.yearly_seasonality = True
        self.changepoints = None

    """
    Make sure start and end dates are in the range and can be
    converted to pandas datetimes. Returns dates in the correct format
    """
    def handle_dates(self, start_date, end_date):


        # Default start and end date are the beginning and end of data
        if start_date is None:
            start_date = self.min_date
        if end_date is None:
            end_date = self.max_date

        try:
            # Convert to pandas datetime for indexing dataframe
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)

        except Exception as e:
            print('Enter valid pandas date format.')
            print(e)
            return

        valid_start = False
        valid_end = False

        # User will continue to enter dates until valid dates are met
        while (not valid_start) & (not valid_end):
            valid_end = True
            valid_start = True

            if end_date < start_date:
                print('End Date must be later than start date.')
                start_date = pd.to_datetime(input('Enter a new start date: '))
                end_date= pd.to_datetime(input('Enter a new end date: '))
                valid_end = False
                valid_start = False

            else:
                if end_date > self.max_date:
                    print('End Date exceeds data range')
                    end_date= pd.to_datetime(input('Enter a new end date: '))
                    valid_end = False

                if start_date < self.min_date:
                    print('Start Date is before date range')
                    start_date = pd.to_datetime(input('Enter a new start date: '))
                    valid_start = False


        return start_date, end_date

    """
    Return the dataframe trimmed to the specified range.
    """
    def make_df(self, start_date, end_date, df=None):

        # Default is to use the object stock data
        if not df:
            df = self.stock.copy()


        start_date, end_date = self.handle_dates(start_date, end_date)

        # keep track of whether the start and end dates are in the data
        start_in = True
        end_in = True

        # If user wants to round dates (default behavior)
        if self.round_dates:
            # Record if start and end date are in df
            if (start_date not in list(df['Date'])):
                start_in = False
            if (end_date not in list(df['Date'])):
                end_in = False

            # If both are not in dataframe, round both
            if (not end_in) & (not start_in):
                trim_df = df[(df['Date'] >= start_date) &
                             (df['Date'] <= end_date)]

            else:
                # If both are in dataframe, round neither
                if (end_in) & (start_in):
                    trim_df = df[(df['Date'] >= start_date) &
                                 (df['Date'] <= end_date)]
                else:
                    # If only start is missing, round start
                    if (not start_in):
                        trim_df = df[(df['Date'] > start_date) &
                                     (df['Date'] <= end_date)]
                    # If only end is imssing round end
                    elif (not end_in):
                        trim_df = df[(df['Date'] >= start_date) &
                                     (df['Date'] < end_date)]


        else:
            valid_start = False
            valid_end = False
            while (not valid_start) & (not valid_end):
                start_date, end_date = self.handle_dates(start_date, end_date)

                # No round dates, if either data not in, print message and return
                if (start_date in list(df['Date'])):
                    valid_start = True
                if (end_date in list(df['Date'])):
                    valid_end = True

                # Check to make sure dates are in the data
                if (start_date not in list(df['Date'])):
                    print('Start Date not in data (either out of range or not a trading day.)')
                    start_date = pd.to_datetime(input(prompt='Enter a new start date: '))

                elif (end_date not in list(df['Date'])):
                    print('End Date not in data (either out of range or not a trading day.)')
                    end_date = pd.to_datetime(input(prompt='Enter a new end date: ') )

            # Dates are not rounded
            trim_df = df[(df['Date'] >= start_date) &
                         (df['Date'] <= end_date.date)]

        return trim_df


    # Basic Historical Plots and Basic Statistics
    def get_stats(self, start_date=None, end_date=None, stats=['Adj. Close']):

        if start_date is None:
            start_date = self.min_date
        if end_date is None:
            end_date = self.max_date

        stock_plot = self.make_df(start_date, end_date)

        ans = []

        for i, stat in enumerate(stats):

            #stat_min = min(stock_plot[stat])
            #stat_max = max(stock_plot[stat])

            #stat_avg = np.mean(stock_plot[stat])

            #date_stat_min = stock_plot[stock_plot[stat] == stat_min]['Date']
            #date_stat_min = date_stat_min[date_stat_min.index[0]]
            #date_stat_max = stock_plot[stock_plot[stat] == stat_max]['Date']
            #date_stat_max = date_stat_max[date_stat_max.index[0]]

            #print('Maximum {} = {:.2f} on {}.'.format(stat, stat_max, date_stat_max))
            #print('Minimum {} = {:.2f} on {}.'.format(stat, stat_min, date_stat_min))
            #print('Current {} = {:.2f} on {}.\n'.format(stat, self.stock.loc[self.stock.index[-1], stat], self.max_date))
            ans.append(self.stock.loc[self.stock.index[-1], stat])

        return ans

    # Method to linearly interpolate prices on the weekends
    def resample(self, dataframe):
        # Change the index and resample at daily level
        dataframe = dataframe.set_index('ds')
        dataframe = dataframe.resample('D')

        # Reset the index and interpolate nan values
        dataframe = dataframe.reset_index(level=0)
        dataframe = dataframe.interpolate()
        return dataframe

    # Remove weekends from a dataframe
    def remove_weekends(self, dataframe):

        # Reset index to use ix
        dataframe = dataframe.reset_index(drop=True)

        weekends = []

        # Find all of the weekends
        for i, date in enumerate(dataframe['ds']):
            if (date.weekday()) == 5 | (date.weekday() == 6):
                weekends.append(i)

        # Drop the weekends
        dataframe = dataframe.drop(weekends, axis=0)

        return dataframe

    # Calculate and plot profit from buying and holding shares for specified date range
    def buy_and_hold(self, start_date=None, end_date=None, nshares=1):

        start_date, end_date = self.handle_dates(start_date, end_date)

        # Find starting and ending price of stock
        start_price = float(self.stock[self.stock['Date'] == start_date]['Adj. Open'])
        end_price = float(self.stock.tail(1)['Adj. Close'])

        # Make a profit dataframe and calculate profit column
        profits = self.make_df(start_date, end_date)
        profits['hold_profit'] = nshares * (profits['Adj. Close'] - start_price)

        # Total profit
        total_hold_profit = nshares * (end_price - start_price)

        #print('{} Total buy and hold profit from {} to {} for {} shares = ${:.2f}'.format
        #      (self.symbol, start_date, end_date, nshares, total_hold_profit))

        return total_hold_profit

    # Create a prophet model without training
    def create_model(self):

        # Make the model
        model = fbprophet.Prophet(daily_seasonality=self.daily_seasonality,
                                  weekly_seasonality=self.weekly_seasonality,
                                  yearly_seasonality=self.yearly_seasonality,
                                  changepoint_prior_scale=self.changepoint_prior_scale,
                                  changepoints=self.changepoints)

        if self.monthly_seasonality:
            # Add monthly seasonality
            model.add_seasonality(name = 'monthly', period = 30.5, fourier_order = 5)

        return model

    # Basic prophet model for specified number of days
    def create_prophet_model(self, days=1, resample=False):

        model = self.create_model()

        # Fit on the stock history for self.training_years number of years
        stock_history = self.stock[self.stock['Date'] > (self.max_date - pd.DateOffset(years = self.training_years))]

        if resample:
            stock_history = self.resample(stock_history)

        model.fit(stock_history)

        # Make and predict for next year with future dataframe
        future = model.make_future_dataframe(periods = days, freq='D')
        future = model.predict(future)

        ans = -1

        if days > 0:
            # Print the predicted price
            print('Predicted Price on {} = ${:.2f}'.format(
                future.loc[future.index[-1], 'ds'], future.loc[future.index[-1], 'yhat']))
            ans = future.loc[future.index[-1], 'yhat']

        return ans
