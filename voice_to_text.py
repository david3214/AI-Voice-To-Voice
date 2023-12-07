import speech_recognition as sr
from pydub import AudioSegment
import os

class SpeechToText:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.filename = self.audio_file.filename
        self.r = sr.Recognizer()
        self.text = None

    def convert_to_wav(self):
        audio = AudioSegment.from_file_using_temporary_files(self.audio_file)
        filename = self.filename.split('.')[0] + '.wav'
        save_path = os.path.join('static', filename)
        audio.export(save_path, format='wav')
        return filename

    def get_text(self):
        if self.filename.split('.')[1] != 'wav':
            self.filename = self.convert_to_wav()
        
        with sr.AudioFile(os.path.join('static', self.filename)) as source:
            audiodata = self.r.record(source)  # read the entire audio file

        try:
            self.text = self.r.recognize_google(audiodata)
            return self.text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return "Could not request results. check your internet connection"