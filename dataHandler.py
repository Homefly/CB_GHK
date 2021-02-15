import pandas as pd

class DataHandler:
    def __init__(self):

        self.marketData = pd.DataFrame(
                      columns=['sequence', 'product_id', 'price',
                               'open_24h', 'volume_24h', 'low_24h',
                               'high_24h', 'volume_30d', 'best_bid', 
                               'best_ask', 'side', 'time', 'trade_id',
                               'last_size', 'predX', 'predDX', 'policy'])  
        self.marketData.set_index('time', inplace=True)
        
        
    def addData(self, marketDatum, predX, predDX, policy):
        #import pdb; pdb.set_trace()
        self.marketData.loc[marketDatum['time']] = marketDatum
        #import pdb; pdb.set_trace()
        self.marketData.loc[marketDatum['time'], ['predX', 'predDX', 'policy']] = \
            [predX, predDX, policy]
    
    @property
    def getData(self):
        return self.marketData

