import socket
import threading
import numpy as np
import whisper
import io
import soundfile as sf
from gtts import gTTS
from playsound import playsound
import torch
import os

# Initialize Whisper model in CPU mode
model = whisper.load_model("base", device="cpu")

'''
def whisper_to_text(audio_data, sample_rate):
    print("we got data from client and whisper_to_text ...")
    with io.BytesIO() as wav_io:
        sf.write(wav_io, audio_data, sample_rate, format='WAV')
        wav_io.seek(0)
        result = model.transcribe(wav_io)
        return result['text']

'''

def whisper_to_text(audio_data, sample_rate):
    # Convert the audio data to a float32 numpy array
    print("we got data from client and whisper_to_text ...")
    audio_data = audio_data.astype(np.float32)

    with io.BytesIO() as wav_io:
        sf.write(wav_io, audio_data, sample_rate, format='WAV')
        wav_io.seek(0)

        # Ensure the data is in FP32 before passing to the model
        wav_io_bytes = wav_io.read()
        audio_tensor = torch.frombuffer(wav_io_bytes, dtype=torch.float32)
        
        result = model.transcribe(audio_tensor)
        return result['text']


def text_to_speech(text):
    tts = gTTS(text)
    tts.save("output.mp3")
    playsound("output.mp3")
    os.remove("output.mp3")

def monitor_keywords(text, keywords, callback):
    for keyword in keywords:
        if keyword in text:
            callback(text)
            break

def process_audio(client_socket, address):
    print(f"Connection from {address} has been established!")
    audio_data = []
    sample_rate = 16000  # Assuming 16000 Hz

    counter = 0
    while True:
        data = client_socket.recv(4096)
        counter = counter + 1
        print(f"{counter} receiving data from {address}")
        if not data:
            print("no data coming from {address}")
            break

        text=whisper_to_text(np.frombuffer(data, dtype=np.int16), sample_rate)
        audio_data.append(text)
        print(text)
    
    if not audio_data:
        print("received nothing from {address}")
        return

    audio_data = np.concatenate(audio_data)
    text = whisper_to_text(audio_data, sample_rate)
    print(f"Transcribed text: {text}")

    def keyword_callback(text):
        nonlocal client_socket
        print(f"Keyword detected in text: {text}")
        client_socket.close()

    monitor_thread = threading.Thread(target=monitor_keywords, args=(text, ['keyword1', 'keyword2'], keyword_callback))
    monitor_thread.start()
    
    text_to_speech(text)
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print("Server is listening on port 5000")

    while True:
        client_socket, address = server_socket.accept()
        client_handler = threading.Thread(target=process_audio, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
