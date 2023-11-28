from flask import Flask, render_template, request, jsonify
from chatgpt import OpenAIChatbot
from eleven_labs import Voices, Models, TTS

app = Flask(__name__)

chatbot = OpenAIChatbot()
tts = TTS('')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.json.get('message')
    print(message)
    # Process the message here (e.g., save to database, perform an action, etc.)
    response_message = chatbot.get_completion(message)
    # tts.set_text(response)
    return jsonify({"message": response_message})

if __name__ == '__main__':
    app.run(debug=True)