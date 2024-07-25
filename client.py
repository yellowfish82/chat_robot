import socket
import pyaudio

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5000))

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

    print("Streaming audio to server...")

    try:
        while True:
            data = stream.read(1024)
            client_socket.sendall(data)
    except KeyboardInterrupt:
        print("Stopping client...")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        client_socket.close()

if __name__ == "__main__":
    start_client()
