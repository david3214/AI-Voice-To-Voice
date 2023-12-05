# I want to clear any audio files in the static folder before the app starts.
# Any file starting with 'output_' or 'recording-' should be deleted.
import os

def clear_old_audio():
    for filename in os.listdir('static'):
        if filename.startswith('output_') or filename.startswith('recording-'):
            os.remove(os.path.join('static', filename))