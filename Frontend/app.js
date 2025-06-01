// DOM Elements
const homeScreen = document.getElementById('homeScreen');
const chatScreen = document.getElementById('chatScreen');
const homeBtn = document.getElementById('homeBtn');
const chatBtn = document.getElementById('chatBtn');
const micButton = document.getElementById('micButton');
const statusText = document.getElementById('statusText');
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

// API Configuration
const API_BASE_URL = 'http://localhost:5000';
const API_ENDPOINTS = {
    chat: `${API_BASE_URL}/api/chat`,
    speech: `${API_BASE_URL}/api/speech`
};

// Speech Recognition Setup
let recognition = null;
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
}

// State
let isRecording = false;
let isListening = false;

// Event Listeners
homeBtn.addEventListener('click', () => showScreen('home'));
chatBtn.addEventListener('click', () => showScreen('chat'));
micButton.addEventListener('click', startListening);
sendButton.addEventListener('click', sendMessage);
messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

// Functions
function showScreen(screen) {
    if (screen === 'home') {
        homeScreen.classList.remove('hidden');
        chatScreen.classList.add('hidden');
        homeBtn.classList.add('bg-gray-100');
        chatBtn.classList.remove('bg-gray-100');
    } else {
        homeScreen.classList.add('hidden');
        chatScreen.classList.remove('hidden');
        homeBtn.classList.remove('bg-gray-100');
        chatBtn.classList.add('bg-gray-100');
    }
}

async function startListening() {
    if (!recognition) {
        addErrorMessage('Speech recognition is not supported in your browser.');
        return;
    }

    if (!isRecording) {
        try {
            isRecording = true;
            micButton.classList.add('recording');
            statusText.textContent = 'Listening...';
            
            // Add active class to orb
            document.querySelector('.orb-container').classList.add('active');
            
            recognition.start();
            
            recognition.onresult = async (event) => {
                const text = event.results[0][0].transcript;
                addMessage(text, 'user');
                await processMessage(text);
            };
            
            recognition.onerror = (event) => {
                console.error('Speech recognition error:', event.error);
                statusText.textContent = `Error: ${event.error}`;
                addErrorMessage(`Speech recognition failed: ${event.error}`);
                stopListening();
            };
            
            recognition.onend = () => {
                stopListening();
            };
            
        } catch (error) {
            console.error('Speech recognition error:', error);
            statusText.textContent = `Error: ${error.message}`;
            addErrorMessage(`Speech recognition failed: ${error.message}`);
            stopListening();
        }
    } else {
        stopListening();
    }
}

function stopListening() {
    if (recognition) {
        recognition.stop();
    }
    isRecording = false;
    isListening = false;
    micButton.classList.remove('recording');
    statusText.textContent = '';
    document.querySelector('.orb-container').classList.remove('active');
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    messageInput.value = '';
    addMessage(message, 'user');
    await processMessage(message);
}

async function processMessage(message) {
    try {
        console.log('Sending chat message:', message);
        const response = await fetch(API_ENDPOINTS.chat, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to get response');
        }
        
        const data = await response.json();
        console.log('Chat response:', data);
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        addMessage(data.response, 'assistant');
    } catch (error) {
        console.error('Chat error:', error);
        addErrorMessage(`Failed to get response: ${error.message}`);
    }
}

function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addErrorMessage(text) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = text;
    chatMessages.appendChild(errorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to handle navigation
function handleNavigation(page) {
    // Remove active class from all buttons
    document.querySelectorAll('.bg-gradient-to-r button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to current page button
    const currentButton = document.querySelector(`button[onclick="window.location.href='${page}.html'"]`);
    if (currentButton) {
        currentButton.classList.add('active');
    }
}

// Add click handlers for navigation buttons
document.querySelectorAll('.bg-gradient-to-r button').forEach(button => {
    button.addEventListener('click', function() {
        const href = this.getAttribute('onclick')?.match(/'([^']+)'/)?.[1];
        if (href) {
            const page = href.replace('.html', '');
            handleNavigation(page);
        }
    });
});

// Initialize active state based on current page
const currentPage = window.location.pathname.split('/').pop().replace('.html', '');
if (currentPage) {
    handleNavigation(currentPage);
}

// Initialize
showScreen('home'); 