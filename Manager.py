#Built in
import asyncio
import matplotlib.pyplot as plt

#3rd Party
from dateutil import parser
from dateutil.relativedelta import relativedelta

#1st Party
from MessageHandler import MessageHandler
from CB_GH import CB_GH
from DataHandler import DataHandler
from RTPlot import RTPlot
from ActionTaker import ActionTaker


async def managerLogic():
    while(True):
        #await a new message
        await mesHand.newMessage()

        #if new data send it to algo
        predX, predDX, policy, algoType = GHFil.run(mesHand.lTick['price'], mesHand.lTick['time'])

        #if new data save data
        history.addData(mesHand.lTick, predX, predDX, policy, algoType) #TODO: make this async or make CSV save async
        

        #animate update and measurement
        #rtPlot.updatePlot(history) #TODO: make this grab from CSV
        
        #buy or sell
        await actionTaker.run(policy) #TODO: make this async

#Main loop
loop = asyncio.get_event_loop()

#initialized values
#lastPolicy = None

filParams = {'x':55854.248527, 'dx':0.449678, 'dt':1., 'g':1.e-2, 'h':1.e-4}
GHFil = CB_GH(**filParams)
history = DataHandler()
mesHand = MessageHandler(loop)
rtPlot = RTPlot()
actionTaker = ActionTaker(loop)

#Add manager to the loop
loop.create_task(managerLogic())

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(mesHandler.close())
    loop.close()