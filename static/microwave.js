let ws;

function initializeWebSocket() {
    ws = new WebSocket("ws://localhost:8000/ws/microwave/state");

    ws.onopen = (event) => {
        console.log("WebSocket opened:", event);
    };

    ws.onmessage = (event) => {
        console.log("Update State")
        const data = JSON.parse(event.data);
        updateState(data);
    };

    ws.onclose = (event) => {
        console.log("WebSocket closed:", event);
    };

    ws.onerror = (event) => {
        console.error("WebSocket error:", event);
    };
}


function updateState(data) {
    document.getElementById('power').innerText = data.power;
    document.getElementById('counter').innerText = data.counter;
    document.getElementById('status').innerText = (data.counter || data.power) > 0 ? "ON" : "OFF";
}

function increasePower() {
    fetch('/power/increase', {method: 'POST'})
    .then(response => response.json())
    .then(data => updateState(data));
}

function decreasePower() {
    fetch('/power/decrease', {method: 'POST'})
    .then(response => response.json())
    .then(data => updateState(data));
}

function increaseCounter() {
    fetch('/counter/increase', {method: 'POST'})
    .then(response => response.json())
    .then(data => updateState(data));
}

function decreaseCounter() {
    fetch('/counter/decrease', {method: 'POST'})
    .then(response => response.json())
    .then(data => updateState(data));
}

function cancelOperation() {
    const token = prompt("Enter your JWT token:");
    fetch('/cancel', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
    .then(response => response.json())
    .then(data => updateState(data));
}
