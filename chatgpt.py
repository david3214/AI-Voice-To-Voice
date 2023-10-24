import openai
import os
from dotenv import load_dotenv

# get OPENAI_KEY from environment variable, in dotenv file
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
GPT_MODELS = {
    "3": "gpt-3.5-turbo",
    "4": "gpt-4"
}
openai.api_key = OPENAI_KEY

# Each instance of the chatbot contains a history of the conversation it has had
class OpenAIChatbot:
    def __init__(self, model=GPT_MODELS["3"]):
        self.model = model
        self.messages = []
        self.messages.append({"role": "system", "content": "You are a helpful chatbot, that will craft answers in a simple way to be understood in voice conversations. Keep your responses to one to two paragraphs"})

    def get_completion(self, prompt, model=GPT_MODELS["3"]):
        self.messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            temperature=0.1,
            stream=True,
        )
        self.messages.append({"role": "assistant", "content": response.choices[0].message["content"]})
        return response.choices[0].message["content"]



if __name__ == '__main__':
    chatbot = OpenAIChatbot()
    print(chatbot.get_completion("Explain the basics of a Markov Decision Process in Value Iteration."))