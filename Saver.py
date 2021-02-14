#!/usr/bin/env python3
import asyncio
from datetime import datetime
from pprintpp import pprint as pp


from copra.websocket import Channel, Client

class SaverTicker(Client):
    def __init__(self, loop):
        
        channel = Channel('ticker', 'LTC-USD')
        super().__init__(loop, channel)
        self.lastTick = None
        self.setProtocolOptions(autoPingInterval= 1, autoPingTimeout = 1)

    def on_message(self, message):
        """
        Keys for 'matches'
        'type', 'trade_id','maker_order_id', 'taker_order_id',
        'side', 'size', 'price', 'product_id', 'sequence',
        'time'
        """
        
        self.lastTick = message      
        #print(message)
        
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    
    Saver = SaverTicker(loop)
    

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(saver.close())
        loop.close()