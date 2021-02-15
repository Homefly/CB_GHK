import asyncio
from filterpy.gh import GHFilter
from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime
import matplotlib.pyplot as plt

#first Party
from Saver import SaverTicker
from CB_GHK import CB_GHK
from dataHandler import DataHandler


async def managerLogic(filter):

    lastMeasureTime = None
    lastPolicy = None
    mostRecentTime = None
    history = DataHandler()
    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    plt.ion()
    plt.show(block=False)

    while(True):
        
        #check for new data. if no knew data, sleep.
        #if new data arrives pass it to be analyzed
        if (saver.lastTick == None) or \
        (mostRecentTime == parser.parse(saver.lastTick['time'])):
            #No new data return control
            await asyncio.sleep(0.01)
        else:

            #if new data send it to algo
            mostRecentTime = parser.parse(saver.lastTick['time'])
            lastPrice = float(saver.lastTick['price'])
            predX, predDX, policy = filter.run(lastPrice, mostRecentTime)
            
            #if new data save data
            history.addData(saver.lastTick, predX, predDX, policy)
            #print(history.getData().head())
        
            #animate update and measurement
            z = list(map(float, history.getData['price'].iloc[-600:]))
            x = list(map(float, history.getData['predX'].iloc[-600:]))
            #print('y ' + str(y))
            plt.cla()
            ax.plot(z)
            ax.plot(x)
            plt.pause(0.01)
        
            #buy or sell
            
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
f = CB_GHK(x=214, dx=0., ddx=0., dt=1.,
             g=.1, h=.02, k = .05)

#Add manager to the loop
loop.create_task(managerLogic(f))

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(saver.close())
    loop.close()