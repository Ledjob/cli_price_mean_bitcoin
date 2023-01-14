# -*- coding: utf-8 -*-
import pandas_ta as ta
import pandas as pd

import click

import ccxt  # noqa: E402

#print('CCXT Version:', ccxt.__version__)

@click.command()
@click.argument("ticker")
@click.option('--timeframe', '-t', type=str,  required=True, help="please enter the timeframe. i.e 1m or 1h")
@click.option('--lookback', '-l', type=int,  default=10, help="please enter the number of value to select "
                                                               "for indicators. 10 last values or 100 last")

def main(ticker, timeframe, lookback):
    exchange = ccxt.kraken()

    # exchange.verbose = True  # uncomment for debugging purposes

    ohlcv = exchange.fetch_ohlcv(f'{ticker}', f'{timeframe}')





    if len(ohlcv):
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        ema = df.ta.ema(length=lookback)
        df = pd.concat([df, ema], axis=1)
        # print(df)

        # Here we are just resetting the indexing for the entire database
        # and reversing the database.

        d = df.loc[::-1].reset_index(drop=True)
        #print(d)
        mean_avg = d['close'].iloc[:lookback].mean()
        std = d['close'].iloc[:lookback].std()
        ema = d[f'EMA_{lookback}'].iloc[0]

        print(f'{lookback} last values mean is: {mean_avg}')
        print(f'{lookback} last values std is: {std}')
        print(f'{lookback} last values for EMA is: {ema}')

        if d["close"].iloc[0] > ema:
            click.secho('price higher than ema', fg="blue", bold=True)

        else:
            click.secho('price under EMA', fg="red", bold=True)

        if d["close"].iloc[0] > std:
            click.secho('price higher than MEAN', fg="blue", bold=True)
            std_dev = d['close'][0] - mean_avg
            print(std_dev)
            print(f'{std_dev/std:.2f} standard dev from the mean')

        else:
            click.secho('price under mean', fg="red", bold=True)
            std_dev = mean_avg - d['close'][0]
            print(std_dev)


        act_price = d['close'][0]
        print(f'actual price: {act_price}')



##### calculate how many times / std dev we are above or velow mean

if __name__ == '__main__':
    main()

