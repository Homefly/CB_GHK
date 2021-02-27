import asyncio
import time
from pprint import pprint

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
            usdSize = float(f'{usd_available:.8f}')
            pprint(usdSize)
            
            if usdSize > 1.: #TODO: change this to min tradable size
                # Place a market order
                try:
                    order = await client.market_order('buy', 'BTC-USD', size=usdSize)
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
            btcSize = float(f'{btc_available:.8f}')
            pprint(btcSize)
            
            if btcSize > 1.e-6: #TODO: change this to min tradable size
                # Place a market order
                try:
                    order = await client.market_order('sell', 'BTC-USD', size=btcSize)
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
    