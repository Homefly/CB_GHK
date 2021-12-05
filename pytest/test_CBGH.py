import asyncio
import json

from copra.websocket import Client, FEED_URL, SANDBOX_FEED_URL
from copra.rest import APIRequestError, Client, URL, SANDBOX_URL
from CBFilter import ActionTaker

import asyncio
import pytest

# from ../ActionTaker import ActionTaker

"""
buy and sell then check that they went through
make sure action taker uses keys for test profile and
"""

loop = asyncio.get_event_loop()
cbpCOM = ActionTaker(loop, channels='', feed_url=SANDBOX_URL)
# cbpCOM.buy_BTC()
"""
with open('keys.json') as f:
    data = json.load(f)
KEY = data['KEY']
SECRET = data['SECRET']
PASSPHRASE = data['PASSPHRASE']
"""


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


def testfunc():
    """
    sdfksdf
    """
    pass

# Action Taker

# create state for if the account has BTC or dollars


def testBuy(event_loop):
    accounts = event_loop.run_until_complete(cbpCOM.get_currency())
    # print(accounts)

    result = event_loop.run_until_complete(cbpCOM.buy_BTC())
    # print(result)

    import ipdb
    ipdb.set_trace()
    assert result == 'not enough usd to trade'
    # check if buy occured correctly


def testSell(event_loop):
    result = event_loop.run_until_complete(cbpCOM.sell_BTC())
    print(result)
    import ipdb
    ipdb.set_trace()
    """
    docstring
    """
    assert result == 'not enough usd to trade'
    # check if buy occured correctly


#loop = event_loop
# loop.close()

"""
    with Client(loop, channels='', feed_url=FEED_URL, auth=True, key=KEY, secret=SECRET,
                passphrase=PASSPHRASE) as client:

        accounts = client.accounts()
        for account in accounts:
            if account['currency'] == 'USD':
                usd_available = float(account['available'])
                pprint(account)
    """

"""
def testsell(event_loop):
    result = event_loop.run_until_complete(cbpCOM.sell_BTC())
    # check if buy occured correctly
"""
"""
with Client(loop, channels='', feed_url=FEED_URL, auth=True, key=KEY, secret=SECRET,
            passphrase=PASSPHRASE) as client:

    accounts = client.accounts()
    for account in accounts:
        if account['currency'] == 'USD':
            usd_available = float(account['available'])
            pprint(account)
"""
