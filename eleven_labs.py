import elevenlabs
from dotenv import load_dotenv
from os import getenv
from enum import Enum
from typing import Generator

load_dotenv()
elevenlabs.set_api_key(getenv('ELEVEN_LABS_API_KEY'))


class Models(Enum):
    '''List of available models'''
    MULTILINGUAL = 'eleven_multilingual_v2'
    ENGLISH = 'eleven_monolingual_v1'


class Voices(Enum):
    '''List of american accent voice names'''
    # Only the american accents are listed here
    RACHEL = 'Rachel'
    CLYDE = 'Clyde'
    DOMI = 'Domi'
    BELLA = 'Bella'
    ANTONI = 'Antoni'
    THOMAS = 'Thomas'
    EMILY = 'Emily'
    ELLI = 'Elli'
    CALLUM = 'Callum'
    PATRICK = 'Patrick'
    HARRY = 'Harry'
    LIAM = 'Liam'
    JOSH = 'Josh'
    ARNOLD = 'Arnold'
    MATILDA = 'Matilda'
    MICHAEL = 'Michael'
    ETHAN = 'Ethan'
    GIGI = 'Gigi'
    FREYA = 'Freya'
    SERENA = 'Serena'
    ADAM = 'Adam'
    NICOLE = 'Nicole'
    JESSIE = 'Jessie'
    RYAN = 'Ryan'
    SAM = 'Sam'
    GLINDA = 'Glinda'


class TTS:
    '''Text to speech class for Eleven Labs API'''

    def __init__(self, text: str = None, text_steam: Generator = None, voice: Voices = Voices.ADAM, model: Models = Models.ENGLISH, stream: bool = True) -> None:
        if text is None and text_steam is None:
            raise ValueError('text or text_stream must be set')
        elif text is not None and text_steam is not None:
            raise ValueError('text and text_stream cannot be set at the same time')
        self.text = text
        self.text_stream = text_steam
        self.voice = voice.value
        self.model = model.value
        self.stream = stream

    def play(self) -> None:
        '''Creates an audio stream from the text or text_stream and plays it'''
        if self.text is not None:
            audio_stream = elevenlabs.generate(text=self.text, voice=self.voice, model=self.model, stream=self.stream)
        else:
            audio_stream = elevenlabs.generate(text=self.text_stream(), voice=self.voice, model=self.model, stream=self.stream)
        elevenlabs.stream(audio_stream)

    def set_text(self, text: str) -> None:
        '''Sets the text to be played'''
        self.text_stream = None
        self.text = text

    def set_text_stream(self, text_stream: Generator) -> None:
        '''Sets the text stream to be played'''
        self.text = None
        self.text_stream = text_stream


if __name__ == '__main__':
    tts = TTS(text='Filler text.')
    for voice in Voices:
        tts.voice = voice.value
        tts.set_text(f'Hello, my name is {voice.value}.')
        tts.play()
