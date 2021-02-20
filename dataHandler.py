import pandas as pd
from datetime import datetime
from pprintpp import pprint as pp
path = './data/'

class DataHandler:
    def __init__(self):

        self.marketData = pd.DataFrame(
                      columns=['sequence', 'product_id', 'price',
                               'open_24h', 'volume_24h', 'low_24h',
                               'high_24h', 'volume_30d', 'best_bid', 
                               'best_ask', 'side', 'time', 'trade_id',
                               'last_size', 'predX', 'predDX', 'policy', 'algoName'])  
        self.marketData.set_index('time', inplace=True)
        
        
    def addData(self, marketDatum, predX, predDX, policy, algoName):
        #import pdb; pdb.set_trace()
        self.marketData.loc[marketDatum['time']] = marketDatum
        #import pdb; pdb.set_trace()
        self.marketData.loc[marketDatum['time'], ['predX', 'predDX', 'policy', 'algoName']] = \
            [predX, predDX, policy, algoName]
        pp(self.marketData.iloc[-1])
        #self.saveData(algoName)
        
    def saveData(self, algoName):
        #write last line to CSV
        today = datetime.utcnow().strftime("%m-%d-%y")
        fileName = f'{today}_{algoName}.csv'
        pathName = path + fileName
        with open(pathName, 'a') as f:
            self.marketData.to_csv(f, header=f.tell()==0)
    
    @property
    def getData(self):
        return self.marketData

