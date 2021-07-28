import asyncio
import websockets
import numpy as np
import cv2
import mss
import mss.tools

connected = set()
fp = "appended_dsdt_unformatted_imgs/"
async def server(websocket, path):
    lastName = None
    while True:
        async for message in websocket:
            if (lastName == None or message != lastName):
                #take screenshot and save as message
                with mss.mss() as sct:
                    sct.shot()
                    img = cv2.imread("monitor-1.png")
                    cv2.imwrite(fp + message + ".png", img)
                lastName = message
                # print (connected)
                # for conn in connected:
                #     print ("sending message: " + str(message))
                #     await conn.send(message)
                print (message)


start_server = websockets.serve(server, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
