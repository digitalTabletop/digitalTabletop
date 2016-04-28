import websockets
import asyncio
import random
import requests
import json

USERS = []

async def test(websocket, path):
    entry = {
        "uid": "".join(random.choice("abcdefghijklmnopqrtstuvwxyz1234567890") for i in range(5)),
        "websocket":websocket,
        "state": 1
    }
    USERS.append(entry)
    print("%s connected as %s" % (websocket.remote_address, entry["uid"]))
    try:
        while True: # while connection open...
            message = await websocket.recv()
            message = json.loads(message)
            if entry["state"] == 1: # authentication state
                if "uname" in message.keys():
                    r = requests.get("http://localhost:5000/user/"+message["uname"]+"/avatar")
                    if r.status_code is not 404:
                        # Update avatar
                        USERS.remove(entry)
                        entry["uname"] = message["uname"]
                        entry["avatar"] = r.text
                        entry["state"] = 2
                        USERS.append(entry)
                await websocket.send(json.dumps({"state":1}))

            elif entry["state"] == 2: # Game state
                if "x" in message.keys() and "y" in message.keys():
                    for user in USERS:
                        response = {
                                    "state" : entry["state"],
                                    "x": message["x"],
                                    "y": message["y"],
                                    "avatar" : entry["avatar"],
                                    "uid": entry["uid"]
                        }
                        await user["websocket"].send(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        USERS.remove(entry)
START_SERVER = websockets.serve(test, '0.0.0.0', 8080)

asyncio.get_event_loop().run_until_complete(START_SERVER)
asyncio.get_event_loop().run_forever()
