from flask import Flask, render_template, request, jsonify
from chatgpt import OpenAIChatbot
from eleven_labs import Voices, Models, TTS

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
    response_message = chatbot.get_completion(message)
    tts.set_text(response_message)
    tts.play()
    return jsonify({"message": response_message})


@app.route('/update_voice', methods=['POST'])
def update_voice():
    data = request.get_json()
    selected_voice = data.get('voice')
    tts.voice = selected_voice
    return jsonify({"message": f"Voice updated to {selected_voice}"})


if __name__ == '__main__':
    app.run(debug=True)
