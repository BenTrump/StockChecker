import matplotlib.pyplot as plt
import datetime as dt
from alpha_vantage.timeseries import TimeSeries
#  import pandas as pd


class Commands:
    def __init__(self):
        self.date_today = dt.date.today()
        self.date_yesterday = dt.date.today() - dt.timedelta(1)

    @staticmethod
    def check(*args):
        print(args)
        ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
        data, meta_data = ts.get_batch_stock_quotes(symbols=args)
        print(data.loc[:, ["1. symbol", "2. price", "4. timestamp"]])
        Calls()

    def daily(self, ticker):
        ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
        data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize="full")
        new_data = data.loc[str(self.date_today) + " 09:31:00":, "4. close"]
        new_data.plot(title="Closing values, 1 min interval")
        plt.xlabel("Eastern Standard Time")
        plt.grid()
        plt.show()
        Calls()

    def change(self, *args):
        for ticker in args[0]:
            ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
            data, meta_data = ts.get_intraday(symbol=ticker.upper(), interval='1min', outputsize="full")
            open_price = data.loc[str(self.date_today) + " 09:31:00", "1. open"]
            close_price = data.iloc[-1, 3]
            percent_change = (close_price - open_price)/open_price*100
            print(ticker.upper() + "  " + "%.2f" % percent_change + "%")


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

        if call[0] == "change":
            command.change(call[1:])

        elif call[0] == "daily":
            command.daily(call[1])

        elif call[0] == "exit":
            return

        else:
            print("invalid command")
            Calls()


test = Calls()
