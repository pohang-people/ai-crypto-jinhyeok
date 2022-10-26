import time
import requests
import pandas as pd
from datetime import datetime
import os

while(1):
    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5')
    book = response.json()
    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids['type'] = 0

    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 

    timestamp = int(data['timestamp'])
    dt = datetime.fromtimestamp(timestamp/1000)
    dt_csvname = dt.strftime('%Y-%m-%d') 

    df = pd.concat([bids,asks])
    # bids.append(asks)
    df.reset_index(drop=True, inplace=True)
    df['timestamp'] = dt

    if not os.path.exists('{}-bithumb-btc-orderbook.csv'.format(dt_csvname)):
        df.to_csv('{}-bithumb-btc-orderbook.csv'.format(dt_csvname), index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv('{}-bithumb-btc-orderbook.csv'.format(dt_csvname), index=False, mode='a', encoding='utf-8-sig', header=False)

    time.sleep(1)
