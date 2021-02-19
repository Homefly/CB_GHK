#!/usr/bin/env python3
import cbpro
import pickle
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
import time

"""
For Public Endpoints, our rate limit is 3 requests per second, up to 6 requests per second in bursts. For Private Endpoints, our rate limit is 5 requests per second, up to 10 requests per second in bursts.
"""

class CBData:
    #Defaults:
    defaultStart = '2021-01-15T18:00:00'
    #defaultStart = '2021-01-22T14:40:00'
    defaultEnd   = '2021-01-22T18:00:00'
    filePath = './data/candles_' + defaultStart + '____' + defaultEnd
    POINTSMAX = 200
    #filePath = './data/candles_' + defaultStart + '_' + defaultEnd
    
    @staticmethod
    def loadData(defaultStart = defaultStart,
                 defaultEnd = defaultEnd, filePath= filePath):
        
        infile = open(filePath, 'rb')
        candles = pickle.load(infile)
        infile.close()
        #candles = pd.DataFrame(dL, columns =
        #    ['time', 'low', 'high', 'open', 'close', 'volume'])
        return candles

    @staticmethod
    def getData(sTime = defaultStart, eTime = defaultEnd, 
                POINTSMAX = POINTSMAX):

        def getNumMins(sTime, eTime):
            td = eTime - sTime
            minutes = int(td.total_seconds()/60)
            return minutes
    
        sTime = parse(sTime)
        eTime = parse(eTime)
        
        numMins = getNumMins(sTime, eTime)
        candles = pd.DataFrame(columns =
            ['time', 'low', 'high', 'open', 'close', 'volume'])
        
        cur = cbpro.PublicClient()
        
        for periodDiv in range(POINTSMAX, numMins, POINTSMAX):
            sPeriod = sTime + timedelta(minutes = periodDiv) -timedelta(minutes = POINTSMAX)
            ePeriod = sTime + timedelta(minutes = periodDiv)

            #download data from coinbase
            dL = cur.get_product_historic_rates(
                'BTC-USD', start = str(sPeriod),
                end  = str(ePeriod)) 
            #200 POINTS MAX
            
            tempCandles = pd.DataFrame(dL, columns =
            ['time', 'low', 'high', 'open', 'close', 'volume'])
            candles = candles.append(tempCandles)
            time.sleep(.34)
            print(periodDiv)
                
        #save data
        outFile = open(filePath,'wb')
        pickle.dump(candles, outFile)
        outFile.close()
        return candles
    
    def cleanData(df):
        #sort data
        df.set_index('time', inplace = True)
        df.sort_index(inplace = True)
        df['del'] = df.index
        df['del'] = df['del'].sub(df.index.min())
        df.drop_duplicates()
        #remove doubles
        #j = list(range(0, 600060, 60))
        
    
    def inspectData():
        pass

if __name__ == '__main__':
    t = CBData.getData()
    #t = CBData.getData()