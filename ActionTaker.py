import asyncio
import time
from pprint import pprint
import math

from copra.rest import APIRequestError, Client
from dateutil.relativedelta import relativedelta

from MessageHandler import MessageHandler

KEY = 'b0a2ecd28e49495776c58b367eec2666'
SECRET = 'xY+xNtOOek0t3i07pLx+f/lTpgQ0iXaBjv4siVxQTFvRMX8aKZU6K2yeG/nleDpGTm0DBzKfSqvtrwmvV148Rg=='
PASSPHRASE = 'm1dqqqfuged'

class ActionTaker:
    def __init__(self, loop):
        self.loop = loop
        self.lastPolicy = None
        #self.lastPolicyChangeTime = lastPolicyChangeTime
        PolicyChangeLockout = relativedelta(minutes = 5)
        
    def round_down(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier
    
    #market buy
    async def buy_BTC(self):
        async with Client(self.loop, auth=True, key=KEY, secret=SECRET,
                          passphrase=PASSPHRASE) as client:
            
            accounts = await client.accounts()
            for account in accounts:
                if account['currency'] == 'USD':
                    usd_available = float(account['available'])
                    pprint(account)
            
            #truncate for min tick size        
            usdSize = self.round_down(usd_available, 2)
            pprint(usdSize)
            
            if usdSize > 1.: #TODO: change this to min tradable size
                # Place a market order
                try:
                    order = await client.market_order('buy', 'BTC-USD', funds=usdSize) #size in btc?
                except APIRequestError as e:
                    print(e)
            else:
                print('not enough usd to trade')
                #TODO: make this a warning or error
            
        return
    
    #market sell
    async def sell_BTC(self):
        async with Client(self.loop, auth=True, key=KEY, secret=SECRET,
                          passphrase=PASSPHRASE) as client:

            accounts = await client.accounts()
            for account in accounts:
                if account['currency'] == 'BTC':
                    btc_available = float(account['available'])
                    pprint(account)
        
            #truncate for min tick size
            btcSize = self.round_down(btc_available, 8)
            pprint(btcSize)
            
            if btcSize > 1.e-6: #TODO: change this to min tradable size
                # Place a market order
                try:
                    order = await client.market_order('sell', 'BTC-USD', size=btcSize) #size in btc?
                except APIRequestError as e:
                    print(e)
            else:
                print('not enough usd to trade')
                #TODO: make this a warning or error
        return
    
    async def run(self, policy):
        #if policy has changed take action.
        if policy != self.lastPolicy:
            if policy == 'long':
                self.loop.create_task(self.buy_BTC())
            elif policy == 'short':
                self.loop.create_task(self.sell_BTC())
        self.lastPolicy = policy

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    at = ActionTaker(loop)

    loop.run_until_complete(at.run(loop))

    loop.close()
    print('done')
    