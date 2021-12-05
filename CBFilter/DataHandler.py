import pandas as pd
from datetime import datetime
from pprintpp import pprint as pp
import csv
import os
import asyncio

from aiofile import async_open

path = './data/'


# TODO: save data in csv that doesn't lock program
class DataHandler:
    def __init__(self, algoName):

        self.marketData = pd.DataFrame(
            columns=['sequence', 'product_id', 'price',
                     'open_24h', 'volume_24h', 'low_24h',
                     'high_24h', 'volume_30d', 'best_bid',
                     'best_ask', 'side', 'time', 'trade_id',
                     'last_size', 'predX', 'predDX', 'policy', 'algoName'])
        self.marketData.set_index('time', inplace=True)

        today = datetime.utcnow().strftime("%m-%d-%y")
        fileName = f'{today}_{algoName}.csv'
        self.pathName = path + fileName
        self.sniffer = csv.Sniffer()

    """        
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
            self.marketData.to_csv(f, header=f.tell()==0) #TODO: change to add only the new portion of self.marketData
    """
    async def saveData(self, lTick, algoData):
        dataToSave = {}
        dataToSave.update(lTick)
        dataToSave.update(algoData)

        file_exists = os.path.isfile(self.pathName)
        if file_exists:
            async with async_open(self.pathName, "a+") as f:
                writer = csv.DictWriter(f, fieldnames=dataToSave.keys())
                if not file_exists:
                    await writer.writeheader()
                    await writer.writerow(dataToSave)
        else:
            async with async_open(self.pathName, "w") as f:
                writer = csv.DictWriter(f, fieldnames=dataToSave.keys())
                if not file_exists:
                    await writer.writeheader()
                    await writer.writerow(dataToSave)

    @property
    def getData(self):
        return self.marketData
