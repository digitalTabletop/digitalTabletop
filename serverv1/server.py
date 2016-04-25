import websockets
import asyncio
import random
import json

COLORS = [
    "red",
    "orange",
    "blue",
    "green",
    "purple"
]

USERS = []

async def test(websocket, path):
    entry = {
        "websocket":websocket,
        "color":random.choice(COLORS),
        "state":None
    }
    USERS.append(entry)
    print("%s connected as %s" % (websocket.remote_address, entry["color"]))
    try:
        while True: # while connection open...
            message = await websocket.recv()
            message = json.loads(message)
            print(message)
            if "x" in message.keys() and "y" in message.keys():
                for user in USERS:
                    response = {"x": message["x"],
                                "y": message["y"],
                                "color": entry["color"]
                    }
                    await user["websocket"].send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        pass
    print("%s disconneced" % websocket.remote_address)
START_SERVER = websockets.serve(test, 'localhost', 8080)

asyncio.get_event_loop().run_until_complete(START_SERVER)
asyncio.get_event_loop().run_forever()
