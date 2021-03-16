import asyncio
from copra.websocket.client import SANDBOX_FEED_URL
import sys
import os
print(sys.path)
# from ../ActionTaker import ActionTaker

"""
buy and sell then check that they went through
"""
loop = asyncio.get_event_loop()
cbpCOM = ActionTaker(loop)
cbpCOM.buy_BTC()


def testfunc():
    """
    sdfksdf

    """
    pass
