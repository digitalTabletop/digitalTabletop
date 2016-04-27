import websockets
import asyncio
import random
import json

COLORS = [
    # "rgb(255, 0, 0)",
    # "rgb(255, 165, 0)",
    # "rgb(0, 0, 255)",
    # "rgb(0, 128, 0)",
    # "rgb(128, 0, 128)",
    "url('archer.png')"
]

USERS = []

async def test(websocket, path):
    entry = {
        "uid": "".join(random.choice("abcdefghijklmnopqrtstuvwxyz1234567890") for i in range(5)),
        "websocket":websocket,
        "color":random.choice(COLORS),
        "state":None
    }
    USERS.append(entry)
    print("%s connected as %s" % (websocket.remote_address, entry["uid"]))
    try:
        while True: # while connection open...
            message = await websocket.recv()
            message = json.loads(message)
            print(message)
            if "x" in message.keys() and "y" in message.keys():
                for user in USERS:
                    response = {"x": message["x"],
                                "y": message["y"],
                                "color": entry["color"],
                                "uid": entry["uid"]
                    }
                    await user["websocket"].send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        USERS.remove(entry)
START_SERVER = websockets.serve(test, '0.0.0.0', 8080)

asyncio.get_event_loop().run_until_complete(START_SERVER)
asyncio.get_event_loop().run_forever()
