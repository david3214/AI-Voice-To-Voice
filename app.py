from flask import Flask, render_template, request, jsonify, url_for
from chatgpt import OpenAIChatbot
from eleven_labs import Voices, Models, TTS
from voice_to_text import SpeechToText
from clear_recordings import clear_old_audio

app = Flask(__name__)

chatbot = OpenAIChatbot()
tts = TTS('')

clear_old_audio()

@app.route('/')
def index():
    return render_template('index.html', voices=[voice.value for voice in Voices])


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    print(message)
    
    response_message = chatbot.get_completion(message)
    tts.set_text(response_message)
    filename = tts.save_audio() 

    # Generate URL for the saved audio
    audio_url = url_for('static', filename=filename, _external=True)  # Generate absolute URL

    # response_message = 'Your audio has been processed'
    return jsonify({'audioUrl': audio_url, 'responseMessage': response_message})


@app.route('/update_voice', methods=['POST'])
def update_voice():
    data = request.get_json()
    selected_voice = data.get('voice')
    tts.voice = selected_voice
    return jsonify({"message": f"Voice updated to {selected_voice}"})


@app.route('/process_audio', methods=['POST'])
def process_audio():
    # Receive and save the audio file
    audio_file = request.files['audio']
    # Process the audio file as needed

    # Convert audio to wav
    stt = SpeechToText(audio_file)
    user_text = stt.get_text()
    print(user_text)
    

    response_message = chatbot.get_completion(user_text)
    tts.set_text(response_message)
    filename = tts.save_audio() 

    # Generate URL for the saved audio
    audio_url = url_for('static', filename=filename, _external=True)  # Generate absolute URL

    # response_message = 'Your audio has been processed'
    return jsonify({'audioUrl': audio_url, 'responseMessage': response_message, 'sentText': user_text})


if __name__ == '__main__':
    app.run(debug=True)
