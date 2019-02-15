import matplotlib.pyplot as plt
import datetime as dt
from alpha_vantage.timeseries import TimeSeries


class Commands:
    """"Allows user to send calls to the Alpha Vantage API

    Each method will retrieve and display a different type of stock information.
    Check: prints the latest price quote for the arguments
    Daily: returns a graph of the stock price for the current day (or last trading day)
    Change: prints a daily percent change for a given stock

    Raises:
        KeyError:
    """
    def __init__(self):
        self.date_today = dt.date.today()
        if self.date_today.weekday() == 0:
            self.date_yesterday = dt.date.today() - dt.timedelta(3)
        elif self.date_today.weekday() == 5:
            self.date_today = self.date_today - dt.timedelta(1)
            self.date_yesterday = self.date_today - dt.timedelta(1)
        elif self.date_today.weekday() == 6:
            self.date_today = self.date_today - dt.timedelta(2)
            self.date_yesterday = self.date_today - dt.timedelta(1)
        else:
            self.date_yesterday = self.date_today - dt.timedelta(1)

    # noinspection PyMethodMayBeStatic
    def check(self, *args):
        ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
        data, meta_data = ts.get_batch_stock_quotes(symbols=args)
        print(data.loc[:, ["1. symbol", "2. price", "4. timestamp"]])
        choose_command()

    def daily(self, ticker):
        try:
            ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
            data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize="full")
            new_data = data.loc[str(self.date_today) + " 09:31:00":, "4. close"]
            new_data.plot(title="Closing values, 1 min interval")
            plt.xlabel("Eastern Standard Time")
            plt.grid()
            plt.show()
        except KeyError:
            print(ticker.upper() + " is an invalid ticker")
        choose_command()

    def change(self, *args):
        for ticker in args[0]:
            try:
                ts = TimeSeries(key='EJ69MPM068NGTJ30', output_format='pandas')
                data, meta_data = ts.get_intraday(symbol=ticker, interval='1min', outputsize="full")
                open_price = data.loc[str(self.date_yesterday) + " 16:00:00", "4. close"]
                close_price = data.iloc[-1, 3]
                percent_change = (close_price - open_price)/open_price*100
                print(ticker.upper() + "  " + "%.2f" % percent_change + "%")
            except KeyError:
                print(ticker.upper() + " is an invalid ticker")
                break
        choose_command()


def choose_command():
    print('')
    command = Commands()
    call = input("$").split(" ")
    if call[0] == "check":
        command.check(', '.join(call[1:]))

    elif call[0] == "change":
        if len(call[1:]) > 5:
            print("Alpha Vantage only allows 5 API calls/minute")
            choose_command()
        else:
            command.change(call[1:])

    elif call[0] == "daily":
        command.daily(call[1])

    elif call[0] == "exit":
        return

    else:
        print("invalid command")
        choose_command()


choose_command()
