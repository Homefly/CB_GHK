from copra.rest import Client
import pickle
import pandas as pd
from datetime import datetime, timedelta
from dateutil.parser import parse
import time
import asyncio
import numpy as np
#from MyDebugTools import rLC

"""
For Public Endpoints, our rate limit is 3 requests per second, up to 6 requests per second in bursts. For Private Endpoints, our rate limit is 5 requests per second, up to 10 requests per second in bursts.
"""
class CBData:
    #Defaults:
    defaultStart = '2020-12-01T0:00:00'
    defaultEnd   = '2020-12-31T23:59:00'
    #defaultEnd   = '2021-01-22T18:00:00'
    filePath = './data/candles_' + defaultStart + '__' + defaultEnd
    POINTSMAX = 300
    granularity = 60 #time in seconds between candles
    product_id = "BTC-USD"
    
    @staticmethod
    def loadData(filePath= filePath):
        
        infile = open(filePath, 'rb')
        candles = pickle.load(infile)
        infile.close()
        #candles = pd.DataFrame(dL, columns =
        #    ['time', 'low', 'high', 'open', 'close', 'volume'])
        return candles
    
    @classmethod
    async def dL(cls, pID, granularity, sPer, ePer):
        #loop = asyncio.get_event_loop()
        loop = asyncio.get_running_loop()
        async with Client(loop) as client:
            dL = await client.historic_rates(pID, granularity, sPer, ePer)
        return dL

    @classmethod
    def getHistD(cls, pID = product_id, sT = defaultStart, eT = defaultEnd):
        sT = parse(sT)
        eT = parse(eT)
        getNumMins = lambda sT, eT : int((eT - sT).total_seconds()/60)
        numMins = getNumMins(sT, eT)
        tInts = np.append(np.arange(numMins, 0, -cls.POINTSMAX), 1)
        
        loop = asyncio.get_event_loop()
        candles = pd.DataFrame()
        
        for x in range(len(tInts) - 1):
            ePeriod = str(sT + timedelta(minutes = int(tInts[x])))
            sPeriod = str(sT + timedelta(minutes = int(tInts[x+1])))
            print(f'{pID=}, {sPeriod=}, {ePeriod=}')

            #download data from coinbase
            dL = loop.run_until_complete(cls.dL(pID, cls.granularity, sPeriod , ePeriod))
            
            #import ipdb; ipdb.set_trace()
            candles = candles.append(pd.DataFrame(dL))
            time.sleep(.4)
        
        candles.columns = \
            ['time', 'low', 'high', 'open', 'close', 'volume']
        
        #cls.saveData(candles)

        return candles
    
    def saveData(candles, filePath = filePath):
        outFile = open(filePath,'wb')
        pickle.dump(candles, outFile)
        outFile.close()
        #import ipdb; ipdb.set_trace()
        candles.to_csv(filePath + '.csv')
    
    def cleanData(df):
        #sort data
        df.set_index('time', inplace = True)
        df.sort_index(inplace = True)
        df['del'] = df.index
        df['del'] = df['del'].sub(df.index.min())
        df.drop_duplicates()
        
    def inspectData():
        pass

if __name__ == '__main__':
    t = CBData.getData()
    #t = CBData.getData()