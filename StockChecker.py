import matplotlib.pyplot as plot
import datetime as dt
from alpha_vantage.timeseries import TimeSeries
import pandas as pd


class Commands:
    def __init__(self):
        self.date_today = dt.date.today()
        self.date_yesterday = dt.date.today() - dt.timedelta(1)

    @staticmethod
    def check(*args):
        ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
        data, meta_data = ts.get_batch_stock_quotes(symbols=args)
        print(data.head())
        Calls()

    @staticmethod
    def daily(ticker):
        ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize="full")
        data["4. close"].plot()
        plot.title("%s closing times, 1 minute interval")
        plot.grid()
        plot.show()
        Calls()


class Calls:
    def __init__(self):
        self.choose_command()

    @staticmethod
    def choose_command():
        print('')
        command = Commands()
        call = input("$").split(" ")
        if call[0] == "check":
            command.check(', '.join(call[1:]))

        elif call[0] == "daily":
            command.daily(call[1])

        elif call[0] == "exit":
            return

        else:
            print("invalid command")
            Calls()


test = Calls()
