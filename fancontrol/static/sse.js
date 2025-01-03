const messagesDiv = document.getElementById('messages');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');

let eventSource;

startButton.addEventListener('click', () => {
    // Start listening to SSE
    eventSource = new EventSource('http://127.0.0.1:5999/event'); // Replace with your server endpoint

    eventSource.onopen = () => {
        addMessage('Connected to SSE server', 'text-success');
        startButton.disabled = true;
        stopButton.disabled = false;
    };

    eventSource.onmessage = (event) => {
        addMessage(`Received: ${event.data}`);
    };

    eventSource.onerror = (error) => {
        addMessage('SSE connection error', 'text-danger');
        eventSource.close();
        startButton.disabled = false;
        stopButton.disabled = true;
    };
});

stopButton.addEventListener('click', () => {
    if (eventSource) {
        eventSource.close();
        addMessage('Disconnected from SSE server', 'text-warning');
        startButton.disabled = false;
        stopButton.disabled = true;
    }
});

function addMessage(message, className = '') {
    const p = document.createElement('p');
    p.textContent = message;
    if (className) p.classList.add(className);

    // Prepend the new message to the top of the container
    messagesDiv.prepend(p);
}