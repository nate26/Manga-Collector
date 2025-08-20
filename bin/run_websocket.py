'''Websocket server that broadcasts messages to all connected clients'''

import asyncio
import websockets

CONNECTIONS = set()

async def echo(websocket):
    '''
    Echoes messages to all connected clients

    Parameters:
    - websocket: WebSocketServerProtocol
        The websocket connection to broadcast messages to
    '''
    if websocket not in CONNECTIONS:
        CONNECTIONS.add(websocket)
    async for message in websocket:
        websockets.broadcast(CONNECTIONS, message)

async def main():
    '''
    Main function to run the websocket server
    '''
    async with websockets.serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
