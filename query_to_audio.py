import os
import json
import requests
import base64
from pydub import AudioSegment
from pydub.playback import play


query = input("Enter your query: ")

api_key = os.getenv("QUERY_TO_AUDIO_API_KEY")

url = "https://api.vectorshift.ai/api/pipelines/run"

headers = {
    "Api-Key": api_key,
}

data = {
    "inputs": json.dumps({
        "iuser": query
    }),
    "pipeline_name": "Query to Audio",
    "username": "kruskakli",
}

response = requests.post(url, headers=headers, data=data)
response = response.json()

# Extract the audio data from the response using the correct key 'oresult'
audio_data = response.get('oresult')
audiob64 = audio_data.get('audio')

if audiob64:
    audio = base64.b64decode(audiob64)
    # Save the audio data as a binary file (important change here)
    output_file = "output_audio.wav"  # Suggest a more appropriate extension
    with open(output_file, "wb") as f:  # 'wb' for binary write
        f.write(audio)
    print(f"Audio data saved as {output_file}")

    sound = AudioSegment.from_wav(output_file)
    play(sound)  # Plays the audio using pydub
   
else:
    print("No audio data found in the response")
