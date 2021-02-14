#!/usr/bin/env python3
import cbpro
import pickle
import pandas as pd

class CBData:
    #Defaults:
    defaultStart = '2021-01-22T14:40:00'
    defaultEnd   = '2021-01-22T18:00:00'
    #filePath = './data/candles_' + defaultStart + '_' + defaultEnd
    
    @staticmethod
    def load(defaultStart = defaultStart, defaultEnd = defaultEnd):
        filePath = './data/candles_' + defaultStart + '_' + defaultEnd
        infile = open(filePath, 'rb')
        dL = pickle.load(infile)
        infile.close()
        candles = pd.DataFrame(dL, columns =
            ['time', 'low', 'high', 'open', 'close', 'volume'])
        return candles
    
    @staticmethod
    def getData(defaultStart = defaultStart, defaultEnd = defaultEnd):
        #load data from file or download it if it doesn't exist
        
        filePath = './data/candles_' + defaultStart + '_' + defaultEnd

        if os.path.exists(filePath):
            #load data
            infile = open(filePath, 'rb')
            dL = pickle.load(infile)
            infile.close()

        else:
            #download data from coinbase
            cur = cbpro.PublicClient()
            dL = cur.get_product_historic_rates(
                'BTC-USD', start = defaultStart, end  = defaultEnd) #200 POINTS MAX

            outFile = open(filePath,'wb')
            pickle.dump(dL, outFile)
            outFile.close()
            
        candles = pd.DataFrame(dL, columns =
            ['time', 'low', 'high', 'open', 'close', 'volume'])
        return candles