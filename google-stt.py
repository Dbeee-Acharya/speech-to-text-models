import io;
from google.oauth2 import service_account
from google.cloud import speech

client = speech.SpeechClient.from_service_account_file('credentials.json')
audioFile = 'recording.wav'

with open(audioFile, 'rb') as f:
    data = f.read()

audio = speech.RecognitionAudio(content = data)

config = speech.RecognitionConfig (
    encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz = 44100,
    enable_automatic_punctuation = True,
    language_code = 'en-US'
)

response = client.recognize(config=config, audio=audio)

print(response)
