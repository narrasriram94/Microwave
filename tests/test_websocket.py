from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_websocket():
    with client.websocket_connect("/ws/microwave/state") as websocket:
        data = websocket.receive_json()
        assert "power" in data
        assert "counter" in data
        
        # Send a close message to signal the server to close the connection
        websocket.send_text("close")

def test_websocket_synchronization():
    with client.websocket_connect("/ws/microwave/state") as websocket1, \
         client.websocket_connect("/ws/microwave/state") as websocket2:
        
        # Increase the microwave power
        response = client.post("/power/increase")
        assert response.status_code == 200

        # Receive data from both websockets
        data1 = websocket1.receive_json()
        data2 = websocket2.receive_json()

        # Check if both websockets received the same data
        assert data1 == data2
        assert "power" in data1
        assert "counter" in data1

        # Send a close message to signal the server to close the connections
        websocket1.send_text("close")
        websocket2.send_text("close")
