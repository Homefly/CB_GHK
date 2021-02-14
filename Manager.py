import Saver
import asyncio
from filterpy.gh import GHFilter
from Saver import SaverTicker
from CB_GHK import CB_GHK
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pytz

#set time zone
#timezone = pytz.timezone("UTC")

async def managerLogic(filter):

    lastMeasureTime = None
    lastPolicy = None
    mostRecentTime = None
    
    #tick update logic
    while(True):
        
        if (saver.lastTick == None) or \
        (mostRecentTime == parser.parse(saver.lastTick['time'])):
            #No new data return contro
            await asyncio.sleep(0.01)
        else:
            #if new data send it to algo
            mostRecentTime = parser.parse(saver.lastTick['time'])
            
            lastPrice = float(saver.lastTick['price'])
            predx, predDX, policy = filter.run(lastPrice, mostRecentTime)
            #print(policy)
            """ 
                #if policy has changed take action.
                if policy != lastPolicy:
                    lastPolicy = policy
            """

#Main loop
loop = asyncio.get_event_loop()

#initialize saver
saver = SaverTicker(loop)

#initialize GHKManager
f = CB_GHK(x=4.23E4, dx=0., ddx=0., dt=1.,
             g=.1, h=.02, k = .05)

#Add manager to the loop
loop.create_task(managerLogic(f))

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(saver.close())
    loop.close()