from datetime import datetime
from pprint import pprint as pp

import copra
from dateutil import parser
from dateutil.relativedelta import relativedelta
from filterpy.gh import GHFilter

from CB_Data import CBData


class CB_GH(GHFilter):
    #data sampling rates
    PREDICTIONPERIOD = relativedelta(minutes = 1)
    
    def __init__(self, x0 = None, dx = None, dt = None, g = None, h = None):
        super().__init__(x=x0, dx=dx, dt=dt, g=g, h=h)
        self.lastPredTime  = None
        self.algoName = f'G:{g}_H:{h}'
        self.signal = None
        
    def getSignal(self):
        if self.dx > 0.:
            signal = 'long'
        elif self.dx < 0.:
            signal = 'short'
        else:
            signal = self.signal
        return signal
    
    def dxBatch(self, price):
        _, dx = self.batch_filter(price)
        return dx
        
    def run(self, z , lastDataTime):
        #if not right type converts to correct type
        if not isinstance(z, float):
            z = float(z)
        if not isinstance(lastDataTime, datetime):   
            lastDataTime = parser.parse(lastDataTime)
        
        #only process data one minute apart else return previous data
        if (self.lastPredTime == None) or lastDataTime  >\
            self.lastPredTime + CB_GH.PREDICTIONPERIOD:
            self.lastPredTime = lastDataTime
            self.x, self.dx = self.update(z)
            self.signal = self.getSignal()
        return self.x, self.dx, self.signal, self.algoName
    
    def primeFil(self, product_id, startDate, g, h):
        #get data
        print('priming Filter')
        marketData = CBData.getHistD(
            pID = product_id, sT = startDate, eT = str(datetime.utcnow()))
        marketData.set_index('time', inplace = True)
        marketData.sort_index(inplace = True)
        
        
        super().__init__(x=marketData['close'].iloc[0], dx=0., dt=1., g=g, h=h)
        
        results = self.batch_filter(marketData['close'])
        #import ipdb; ipdb.set_trace()
        
        filParams = {'x0':results[-1][0], 'dx':results[-1][1], 'dt':1., 'g':g, 'h':h}
        pp('Filter Initialization Params:')
        pp(filParams)
        return filParams


if __name__ == '__main__':
    pass
