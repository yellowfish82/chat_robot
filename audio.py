import pyaudio
import wave
from datetime import datetime

# 创建PyAudio对象
p = pyaudio.PyAudio()

# 打开音频流
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("正在录音，按Ctrl+C取消...")

# 准备记录音频
frames = []

try:
    for i in range(0, int(RATE / CHUNK * 10)):  # 录制10秒声音
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    pass

# 停止并关闭音频流
stream.stop_stream()
stream.close()
p.terminate()

print("录音结束.")

# 将录音保存为WAV文件
now=datetime.now()
timestamp = now.strftime('%Y%m%d%H%M%S%f')[:-3]
audio_file_name='./records/'+timestamp+'.wav'
wf = wave.open(audio_file_name, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()