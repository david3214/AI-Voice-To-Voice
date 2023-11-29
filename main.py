from chatgpt import OpenAIChatbot
from eleven_labs import Voices, Models, TTS


def main():
    chatbot = OpenAIChatbot()
    tts = TTS('')

    while True:
        user_input = input('User: ')
        if user_input == 'exit':
            break
        response = chatbot.get_completion(user_input)
        print(f'Chatbot:\n{response}')
        tts.set_text(response)
        tts.play()


if __name__ == '__main__':
    main()
