#1st Party
import asyncio
import matplotlib.pyplot as plt

#2nd Party
from dateutil import parser
from dateutil.relativedelta import relativedelta

#3rd Party
from MessageHandler import MessageHandler
from CB_GHK import CB_GHK
from dataHandler import DataHandler
from RTPlot import RTPlot


async def managerLogic():
    while(True):
        #await a new message
        await mesHand.newMessage()

        #if new data send it to algo
        predX, predDX, policy = GHKFil.run(mesHand.lTick['price'], mesHand.lTick['time'])

        #if new data save data
        history.addData(mesHand.lTick, predX, predDX, policy)

        #animate update and measurement
        rtPlot.updatePlot(history)
        
        #buy or sell
        """ 
        #if policy has changed take action.
        if policy != lastPolicy:
            #spawn a new async task to send buy or sell to exchange
            lastPolicy = policy
        """

#Main loop
loop = asyncio.get_event_loop()

#initialized values
#lastPolicy = None

filParams = {'x':214., 'dx':0., 'ddx':0., 'dt':1., 'g':.1, 'h':.02, 'k':.05}
GHKFil = CB_GHK(**filParams)
history = DataHandler()
mesHand = MessageHandler(loop)
rtPlot = RTPlot()

#Add manager to the loop
loop.create_task(managerLogic())

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(mesHandler.close())
    loop.close()