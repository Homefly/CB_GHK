#Built in
import asyncio
import matplotlib.pyplot as plt

#3rd Party
from dateutil import parser
from dateutil.relativedelta import relativedelta
from pprint import pprint as pp

#1st Party
from MessageHandler import MessageHandler
from CB_GH import CB_GH
from DataHandler import DataHandler
#from RTPlot import RTPlot
from ActionTaker import ActionTaker

#params:
pair = 'BTC-USD'
g = .0005
h = 4.973799150320701e-08
startDate = '2021-02-13T23:59:00'


async def managerLogic():
    GHFilLast = 'None'
    while(True):
        await mesHand.newMessage()
        
        #if new data send it to algo
        predX, predDX, policy, algoType = GHFil.run(mesHand.lTick['price'], mesHand.lTick['time'])
        #pp(mesHand.lTick)
        #pp(f"{predX=} {predDX=}")
        if repr(GHFil)!= GHFilLast:
            print(repr(GHFil))
            pp(mesHand.lTick['time'])
            GHFilLast = repr(GHFil)
        
        #if new data save data
        loop.create_task(history.saveData(
            mesHand.lTick, algoData={'predX':predX, 'predDX':predDX, 'policy':policy, 'algoType':algoType}))

        #animate update and measurement
        #rtPlot.updatePlot(history) #TODO: make this grab from CSV
        
        #buy or sell
        loop.create_task(actionTaker.run(policy))

#Main loop
loop = asyncio.get_event_loop()

#initialized values
#filParams = {'x0':55826.934978, 'dx':-0.001478, 'dt':1., 'g':1.e-2, 'h':1.e-4}

GHFil = CB_GH()
filParams = GHFil.primeFil(pair, startDate, g, h)
GHFil = CB_GH(**filParams)

"""
history = DataHandler()
mesHand = MessageHandler(loop)
rtPlot = RTPlot()
"""
actionTaker = ActionTaker(loop)
history = DataHandler(GHFil.algoName)
mesHand = MessageHandler(loop, pair)

#Add manager to the loop
loop.create_task(managerLogic())

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.run_until_complete(mesHand.close())
    loop.close()