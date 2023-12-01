let uniqueCounter = 0;
let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let audioStream;

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            isRecording = true;
            audioStream = stream; // Store the stream to stop it later
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = handleRecordingStop;
            mediaRecorder.start();
        })
        .catch(error => {
            console.error("Error accessing the microphone", error);
        });
}

function handleRecordingStop() {
    // Convert audio chunks to a single audio Blob
    const audioBlob = new Blob(audioChunks, { type: 'audio/mpeg' });
    const audioUrl = URL.createObjectURL(audioBlob);

    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.mp3');

    fetch('/process_audio', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        if (data.sentText){
            addChatBubble(data.sentText, true); // true indicating it's the user's message
            handleAudioUrl(audioUrl); // Call the function to handle the recorded audio URL
        }

        if (data.responseMessage) {
            addChatBubble(data.responseMessage, false); // false indicating it's not the user's message
        }

        if (data.audioUrl) {
            // const audioPlayer = document.getElementById('audio-playback');
            // audioPlayer.src = data.audioUrl;
            // audioPlayer.play();
            playButton = handleAudioUrl(data.audioUrl);
            togglePlayStop(data.audioUrl, playButton);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function stopRecording() {
    isRecording = false;
    mediaRecorder.stop(); // Stop the media recorder
    audioStream.getTracks().forEach(track => track.stop()); // Stop the media stream
}

// Event handler for the microphone icon
document.querySelector('.mic-icon').addEventListener('click', () => {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
});


function togglePlayStop(audioUrl, playButton) {
    const audioPlayer = document.getElementById('audio-playback');
    if (audioPlayer.src !== audioUrl) {
        // If a new audio, change the source
        audioPlayer.src = audioUrl;
    }
    console.log('audioPlayer.paused: ' + audioPlayer.paused)
    if (audioPlayer.paused) {
        console.log('Playing: ' + playButton)
        audioPlayer.play();
        playButton.textContent = '■'; // Unicode for the stop square
        audioPlayer.setAttribute('data-playing-button-id', playButton.id);
    } else {
        console.log('Pausing: ' + playButton)
        audioPlayer.pause();
        playButton.textContent = '▶️'; // Unicode for the right-pointing triangle
        
        audioPlayer.removeAttribute('data-playing-button-id');
    }
}


function handleAudioUrl(audioUrl) {
    // Example: Attach the audio URL to the last sent message
    let firstMessage = document.querySelector('.chat-history').firstChild;
    let playButton;
    // if firstmessage is a #text node, get the next sibling
    if (firstMessage.nodeType === Node.TEXT_NODE) 
        firstMessage = firstMessage.nextSibling;
    if (firstMessage) {
        console.log(firstMessage)
        playButton = firstMessage.querySelector('.play-audio');
        user = firstMessage.classList.contains('user');
        userText = user ? ' user' : ' other';
        if (!playButton)
            playButton = document.createElement('button');
            playButton.className = 'play-audio' + userText;
            playButton.textContent = '▶️';
            playButton.id = 'play-button-' + uniqueCounter++;
            firstMessage.appendChild(playButton);
        playButton.onclick = () => togglePlayStop(audioUrl, playButton);
    }
    return playButton;
}

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
        if (data.responseMessage)
            addChatBubble(data.responseMessage, false); // false indicating it's not the user's message
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// End of audio events
document.addEventListener('DOMContentLoaded', function() {
    // Get the audio element
    const audioPlayer = document.getElementById('audio-playback');

    // Set up the event listener for when audio ends
    audioPlayer.addEventListener('ended', function() {
        this.currentTime = 0;
        this.pause();
        // Get the ID of the playing button from the data attribute
        const playingButtonId = this.getAttribute('data-playing-button-id');
        if (playingButtonId) {
            // Find the button by ID and reset its text content
            const playingButton = document.getElementById(playingButtonId);
            if (playingButton) {
                playingButton.textContent = '▶️';
            }
        }

        // Clear the attribute since the audio has ended
        this.removeAttribute('data-playing-button-id');
    });
});


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

    });

    var audioPlayer = document.getElementById('audio-playback');

    audioPlayer.addEventListener('error', (e) => {
        console.error('Error loading audio:', e);
    });
});

// Change Voice
document.addEventListener('DOMContentLoaded', function() {
    const voiceButtons = document.querySelectorAll('.voice-button');

    voiceButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedVoice = button.dataset.voice;

            // Remove the 'active' class from all buttons
            voiceButtons.forEach(btn => {
                btn.classList.remove('active');
            });

            // Add the 'active' class to the clicked button
            button.classList.add('active');

            updateVoice(selectedVoice);
        });
    });

    function updateVoice(voice) {
        // Send the selected voice to the server
        fetch('/update_voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ voice: voice }),
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Log the response message
        })
        .catch(error => {
            console.error('Error updating voice:', error);
        });
    }
});
