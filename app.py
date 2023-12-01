from flask import Flask, render_template, request, jsonify, url_for
from chatgpt import OpenAIChatbot
from eleven_labs import Voices, Models, TTS
import os

app = Flask(__name__)

chatbot = OpenAIChatbot()
tts = TTS('')


@app.route('/')
def index():
    return render_template('index.html', voices=[voice.value for voice in Voices])


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    print(message)
    # Process the message here (e.g., save to database, perform an action, etc.)
    # response_message = chatbot.get_completion(message)
    response_message = "This is a response message"
    # tts.set_text(response_message)
    # filename = tts.save_audio()

    filename = "audio.mp3"
    audio_url = url_for('static', filename=filename)  # Generate URL
    print(audio_url)
    return jsonify({'audioUrl': audio_url, 'responseMessage': response_message})


@app.route('/update_voice', methods=['POST'])
def update_voice():
    data = request.get_json()
    selected_voice = data.get('voice')
    tts.voice = selected_voice
    return jsonify({"message": f"Voice updated to {selected_voice}"})


# @app.route('/process_audio', methods=['POST'])
# def process_audio():
#     audio_file = request.files['audio']
#     # Process the audio file as needed
#     # TODO: implement the Speech to text here

#     sent_text = "You said Someting"; # audio to text
#     # response_message = chatbot.get_completion(text)
#     response_message = "This is a response message"
#     # tts.set_text(response_message)
#     # filename = tts.save_audio()

#     filename = "sent_audio.mp3"
#     if audio_file.filename != '':
#         print('Saving file to static folder')
#         audio_file.save(filename)

#     filename = 'audio.mp3'
#     audio_url = url_for('static', filename=filename)  # Generate URL
#     return jsonify({'audioUrl': audio_url, 'sentText': sent_text, 'responseMessage': response_message})


@app.route('/process_audio', methods=['POST'])
def process_audio():
    # Receive and save the audio file
    audio_file = request.files['audio']
    # Process the audio file as needed
    # TODO: implement the Speechto text here

    sent_text = "You said Someting"; # audio to text
    # response_message = chatbot.get_completion(text)
    response_message = "This is a response message"
    # tts.set_text(response_message)
    # filename = tts.save_audio() 

    # TODO: Remove this section and replace with tts audio
    filename = audio_file.filename
    save_path = os.path.join('static', filename)  # Assuming you have a 'static' folder
    audio_file.save(save_path)

    # Generate URL for the saved audio
    audio_url = url_for('static', filename=filename, _external=True)  # Generate absolute URL

    response_message = 'Your audio has been processed'
    return jsonify({'audioUrl': audio_url, 'responseMessage': response_message, 'sentText': 'You said something'})


if __name__ == '__main__':
    app.run(debug=True)
