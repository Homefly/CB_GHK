import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG

#1st party
from CBFilter.data_handler.CB_Data import CBData
from CB_GH import CB_GH

#load Coinbase Data
defaultStart = '2021-02-01T0:00:00'
defaultEnd   = '2021-02-28T18:00:00'
#filePath = './data/candles_' + defaultStart + '__' + defaultEnd
filePaths =   ['data/candles_2021-02-01T0:00:00__2021-02-26T23:59:00',
               'data/candles_2021-01-01T0:00:00__2021-01-31T23:59:00',
               'data/candles_2020-12-01T0:00:00__2020-12-31T23:59:00']
#format coinbase data
cBTC = CBData.loadData(filePaths[0])
for x in range(len(filePaths) - 1):
    cBTC = cBTC.append(CBData.loadData(filePaths[x+1]))
cBTC['time'] = pd.to_datetime(cBTC['time'], unit ='s')
cBTC.rename(columns={"time": "Time", "low":"Low", "high":"High", "open":"Open", "close":"Close",
"volume":"Volume"}, inplace = True)
cBTC.set_index('Time', inplace = True)
cBTC.sort_index(inplace = True)
#import ipdb; ipdb.set_trace()


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()
            
class BTGHFil(Strategy):

    def init(self):
        def dxBatch(price):
            #filParams = {'x0':33000, 'dx':0.0, 'dt':1., 'g':2.e-2, 'h':1.e-6}
            #filParams = {'x0':33000, 'dx':0.0, 'dt':1., 'g':001.5e-3, 'h':1.126e-6}
            #filParams = {'x0':32640, 'dx':0.0, 'dt':1., 'g':.001, 'h':5.00e-7}
            #filParams = {'x0':29000, 'dx':0.0, 'dt':1., 'g':.001, 'h':5.00e-7}
            #filParams = {'x0':29000, 'dx':0.0, 'dt':1., 'g':.0005, 'h':1.2500e-7}
            #filParams = {'x0':29000, 'dx':0.0, 'dt':1., 'g':.0002, 'h':8.881784197001252e-09}
            filParams = {'x0':price[0], 'dx':0.0, 'dt':1., 'g':.0005, 'h':4.973799150320701e-08}
            #.0005
            #.0002
            GHFil = CB_GH(**filParams)
            results = GHFil.batch_filter(price)
            #import ipdb; ipdb.set_trace()
            #x = pd.Series(results[:,0])
            sdx = pd.Series(results[:,0]).diff()[1:]
            sdx = sdx.rolling(window=30).mean()
            dx = results[:,1][1:] #get only the dx terms and remove the first value which is a repeat of initialization value
            
            return dx
        #time = self.data.Time
        price = self.data.Close
        self.dx = self.I(dxBatch, price)
        #call filter primer to set filParams
        
    def next(self):
        #import ipdb; ipdb.set_trace()
        if self.dx > 0.0 and self.position.size <= 0:
            self.buy()
        elif self.dx < -0.0 and self.position.size > 0:
            self.sell()


bt = Backtest(cBTC, BTGHFil, commission=.0035,
              exclusive_orders=True, cash = 1.e7,)
stats = bt.run()
print(stats)
bt.plot()