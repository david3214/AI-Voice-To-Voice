# AI-Voice-To-Voice

This project utilizes a combination of technologies to enable voice-to-voice interactions. Here's an overview of the key components:

## Project Structure

- **app.py**: The main application file that orchestrates the interaction between the voice-to-text model, ChatGPT API, and ElevenLabs AI. It uses Flask as the web framework.
- **chatgpt.py**: A module that encapsulates the functionality of interacting with the OpenAI Chatbot using the ChatGPT API.
- **elevenlabs.py**: A module that encapsulates the functionality of interacting with the ElevenLabs API for text-to-speech (TTS) conversion.
- **voice_to_text.py**: A module that provides functionality for converting spoken words into text using the ElevenLabs API.

### Running the Application

To run the application, execute the following command in your terminal:

```bash
python app.py
```

## Usage

- Open the application in a web browser by navigating to http://127.0.0.1:5000/.
- Choose a voice from the available options on the homepage.
- Interact with the system by entering your message in the provided text box and clicking the "Send" button. Or pressing the microphone icon, speaking your message, then clicking again to send the message.

## API Endpoints

- /: Renders the homepage with voice selection options.
- /send_message (POST): Accepts a JSON payload with a user message, processes it, generates a response, and provides a link to the corresponding audio.
- /update_voice (POST): Updates the selected voice based on user preference.
- /process_audio (POST): Processes an uploaded audio file, converts it to text, generates a response, converts the response to voice, and provides the corresponding audio link.

## Dependencies

- Flask
- ChatGPT API
- ElevenLabs API
- Python-dotenv
- Google Cloud Services
- pydub
- ffmpeg or avconv