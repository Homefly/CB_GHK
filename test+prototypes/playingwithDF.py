import pandas as pd

infoDict = {'type': 'ticker', 'sequence': 6821958154, 'product_id': 'LTC-USD', 'price': '213.75', 'open_24h': '218.38', 'volume_24h': '973857.02645874', 'low_24h': '185.72', 'high_24h': '220.49', 'volume_30d': '17885599.32089389', 'best_bid': '213.74', 'best_ask': '213.75', 'side': 'buy', 'time': '2021-02-15T21:44:29.891570Z', 'trade_id': 54958944, 'last_size': '1.00875289'}

md = pd.DataFrame(
              columns=['sequence', 'product_id', 'price',
                       'open_24h', 'volume_24h', 'low_24h',
                       'high_24h', 'volume_30d', 'best_bid', 
                       'best_ask', 'side', 'time', 'trade_id',
                       'last_size'])  
md.set_index('time', inplace=True)
import pdb; pdb.set_trace()
md.assign(infoDict)


md.head()