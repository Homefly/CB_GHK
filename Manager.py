#1st Party
import asyncio
from datetime import datetime
import matplotlib.pyplot as plt

#2nd Party
from filterpy.gh import GHFilter
from dateutil import parser
from dateutil.relativedelta import relativedelta

#3rd Party
from MessageHandler import MessageHandler
from CB_GHK import CB_GHK
from dataHandler import DataHandler


async def managerLogic():
    while(True):
    
        #await a new message:
        await mesHand.newMessage()

        #if new data send it to algo
        #mostRecentTime = parser.parse(mesHand.lTick['time'])
        #lastPrice = float(mesHand.lTick['price'])
        predX, predDX, policy = GHKFil.run(mesHand.lTick['price'], mesHand.lTick['time'])

        #if new data save data
        history.addData(mesHand.lTick, predX, predDX, policy)

        #animate update and measurement
        z = list(map(float, history.getData['price'].iloc[-600:]))
        x = list(map(float, history.getData['predX'].iloc[-600:]))
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

#initialized values
lastMeasureTime = None
lastPolicy = None
mostRecentTime = None

filParams = {'x':214, 'dx':0., 'ddx':0., 'dt':1., 'g':.1, 'h':.02, 'k':.05}
GHKFil = CB_GHK(**filParams)
history = DataHandler()
mesHand = MessageHandler(loop)

fig, ax = plt.subplots()  # Create a figure containing a single axes.
plt.ion()
plt.show(block=False)


#Add manager to the loop
loop.create_task(managerLogic())

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(mesHandler.close())
    loop.close()