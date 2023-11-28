
function addChatBubble(message, user) {
    var chatHistory = document.getElementById('chat-history');
    var bubble = document.createElement('div');
    bubble.className = 'chat-bubble' + (user ? ' user' : ' other');
    bubble.textContent = message;
    
    // Prepend the new message to keep the order correct
    if (chatHistory.firstChild) {
        chatHistory.insertBefore(bubble, chatHistory.firstChild);
    } else {
        chatHistory.appendChild(bubble);
    }

    // Optional: Scroll to the bottom only if the user is already near the bottom
    if (chatHistory.scrollHeight - chatHistory.scrollTop < window.innerHeight) {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
}

function sendMessageToServer(message) {
    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "message": message })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        addChatBubble(data.message, false); // false indicating it's not the user's message
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Chat bubble creation
document.addEventListener('DOMContentLoaded', function() {
    var sendButton = document.querySelector('.send-button');
    var chatInput = document.getElementById('chat-input');

    sendButton.addEventListener('click', function() {
        var message = chatInput.value.trim();
        if (message) {
            addChatBubble(message, true); // Add user's message to chat
            sendMessageToServer(message); // Send the message to the server
            chatInput.value = ''; // Clear the input field after sending
        }
    });

    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendButton.click();
        }
    });

});

// Open/close sidebar
document.addEventListener('DOMContentLoaded', function() {
    var hamburger = document.querySelector('.hamburger-button');
    var sidebar = document.getElementById('sidebar');

    hamburger.addEventListener('click', function() {
        var sidebarWidth = sidebar.style.width;

        if (sidebarWidth === '250px' || sidebarWidth === "") {
            sidebar.style.width = '0';
            // Adjust main-content margin if necessary
            document.querySelector('.main-content').style.marginLeft = '75px';
        } else {
            sidebar.style.width = '250px';
            // Adjust main-content margin if necessary
            document.querySelector('.main-content').style.marginLeft = '270px'; // 250px + 20px margin
        }
    });
});

// Clicking Mic icon
document.addEventListener('DOMContentLoaded', function() {
    var micIcon = document.querySelector('.mic-icon');
    var chatInput = document.getElementById('input-group');
    var listeningIndicator = document.getElementById('listening-indicator');

    micIcon.addEventListener('click', function() {
        // Toggle visibility of chat input and listening indicator
        if (chatInput.style.display === 'none') {
            chatInput.style.display = 'flex';
            listeningIndicator.style.display = 'none';
        } else {
            chatInput.style.display = 'none';
            listeningIndicator.style.display = 'flex';
        }

        // Here you can add actual voice recognition functionality
    });
});

