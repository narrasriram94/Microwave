from fastapi import WebSocket, Depends, APIRouter, WebSocketDisconnect
from api.dependencies.microwave_helpers import get_microwave_state
from api.events import state_change_event

router = APIRouter()

connected_clients = []  # Keep track of connected clients

@router.websocket("/ws/microwave/state")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)

    # Send the microwave state immediately after connection
    data = get_microwave_state()
    await websocket.send_json(data)

    while True:
        # Check for incoming messages from the client
        try:
            message = await websocket.receive_text()
            if message == "close":
                await websocket.close()
                return
        except WebSocketDisconnect:
            connected_clients.remove(websocket)
            break

        # Wait for the state change event
        await state_change_event.wait()

        # Clear the event after handling
        state_change_event.clear()

        # Send the updated state to all connected clients
        data = get_microwave_state()
        for client in connected_clients:
            await client.send_json(data)

