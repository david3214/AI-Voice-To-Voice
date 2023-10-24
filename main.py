from chatgpt import OpenAIChatbot
from elevel_labs import Voices, Models, TTS

def main():
  chatbot = OpenAIChatbot()
  tts = TTS('')

  while True:
    user_input = input('User: ')
    if user_input == 'exit':
      break
    response = chatbot.get_completion(user_input)
    tts.set_text(response)

  


if __name__ == '__main__':
  main()