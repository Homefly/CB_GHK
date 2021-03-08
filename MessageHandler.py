import asyncio
from datetime import datetime

from copra.websocket import Channel, Client
from dateutil import parser
from pprintpp import pprint as pp


class MessageHandler(Client):
    def __init__(self, loop, newMessageFut=None):
        channel = Channel('ticker', 'BTC-USD')
        super().__init__(loop, channel)
        self.lTick = None
        self.setProtocolOptions(autoPingInterval=1, autoPingTimeout=2)
        self.lastNewMessageTime = None

    def on_message(self, message):
        """
        Keys for 'matches'
        'type', 'trade_id','maker_order_id', 'taker_order_id',
        'side', 'size', 'price', 'product_id', 'sequence',
        'time'
        """
        
        self.lTick = message

    async def newMessage(self):
        # checks for a new message every milisecond
        while(True):
            if (self.lTick == None) or\
                not ('time' in self.lTick) or\
                    (self.lastNewMessageTime == parser.parse(self.lTick['time'])):

                # No new data return control
                await asyncio.sleep(0)
            else:
                self.lastNewMessageTime = parser.parse(self.lTick['time'])
                break

        return True


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    Saver = MessageHandler(loop)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(MessageHandler.close())
        loop.close()
