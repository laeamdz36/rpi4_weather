const socket = new WebSocket("ws://" + window.location.hostname + ":8000/ws");

socket.onmessage = function(event) {
    console.log("Datos recibidos:", event.data);
};

socket.onerror = function(error) {
    console.error("Error WebSocket:", error);
};
