import websocket, json

def on_open(ws):
    print("opened connection")
    """
    subscribe_message = {
        "type": "subscribe",
        "channels": [
            {
                "name": "ticker",
                "product_ids": [
                    "BTC-USD"
                ]
            }
        ]
    }
    heart = {
        "type": "subscribe",
        "channels": [{ "name": "heartbeat", "product_ids": ["ETH-EUR"] }]
    }
    
    subscribe_messageK = {
         "event": "subscribe",
          "pair": [
            "XBT/USD"
          ],
          "subscription": {
            "name": "ticker"
          }
        }
    """
    heart = {
        "type": "subscribe",
        "channels": [{ "name": "heartbeat", "product_ids": ["ETH-EUR"] }]
    }
    ws.send(json.dumps(heart))
    
def on_message(ws, message):
    print("received message")
    print(json.loads(message))

socket = "wss://ws-feed.pro.coinbase.com"
socketK = "wss://ws.kraken.com"

ws = websocket.WebSocketApp(socket, 
                            on_open = on_open, on_message = on_message)

ws.run_forever()