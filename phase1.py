import time
import requests
import pandas as pd
from datetime import datetime
import os
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def init_session():
    session = requests.Session()
    retry = Retry(connect=5, backoff_factor=0.1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    return session

session = init_session()

while(1):   
    book = {}
    try:
        response = session.get('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5', headers = { 'User-Agent': 'Mozilla/5.0' }, verify = False )
    except:
        time.sleep(61)
        continue
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
    df.reset_index(drop=True, inplace=True)
    df['timestamp'] = dt

    if not os.path.exists('{}-bithumb-btc-orderbook.csv'.format(dt_csvname)):
        df.to_csv('{}-bithumb-btc-orderbook.csv'.format(dt_csvname), index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv('{}-bithumb-btc-orderbook.csv'.format(dt_csvname), index=False, mode='a', encoding='utf-8-sig', header=False)

    time.sleep(1)
