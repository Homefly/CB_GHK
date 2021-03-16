#Built in
from datetime import datetime

#3nd Party
from filterpy.gh import GHKFilter
import copra
from dateutil.relativedelta import relativedelta
from dateutil import parser

class CB_GHK(GHKFilter):
    #data sampling rates
    PREDICTIONPERIOD = relativedelta(minutes = 1)
    
    def __init__(self, x, dx, ddx, dt, g, h, k):
        self.gHK = GHKFilter(
            x, dx, ddx, dt, g, h, k)
        self.x = None
        self.dx = None
        self.signal = None
        self.lastPredTime  = None
        
    def getSignal(self): 
        if self.dx > 0:
            signal = 'long'
        else:
            signal = 'short'
        return signal
        
    def run(self, z , lastDataTime):
        #if not right type converts to correct type
        if not isinstance(z, float):
            z = float(z)
        if not isinstance(lastDataTime, datetime):   
            lastDataTime = parser.parse(lastDataTime)
        
        #only process data one minute apart else return previous data
        print('new data: ' + str(lastDataTime))
        if (self.lastPredTime == None) or lastDataTime  >\
            self.lastPredTime + CB_GHK.PREDICTIONPERIOD:
            
            self.lastPredTime = lastDataTime
            self.x, self.dx = self.gHK.update(z)
            print('new prediction: ' + str(self.x) + ' time: ' + str(self.lastPredTime))
            self.signal = self.getSignal()
        return self.x, self.dx, self.signal


if __name__ == '__main__':
    pass