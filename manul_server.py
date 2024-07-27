import os
import time
import whisper
import ollama
import pyttsx3
import ChatTTS
import torch
import torchaudio
import soundfile as sf
import sounddevice as sd

# 指定要监控的目录
monitor_directory = "./records"  # 修改为你的目录路径
chat_reply_directory = "./robot_reply"  # 修改为你的目录路径
llm_model = "llama3.1"

# 初始化上一次检查的文件集合
last_files = set(os.listdir(monitor_directory))

# Initialize Whisper model in CPU mode
# model = whisper.load_model("base", device="cpu")

model = whisper.load_model("base")
engine = pyttsx3.init()

def check_new_files(directory):
    # 获取当前目录下的所有文件
    current_files = set(os.listdir(directory))
    global last_files
    # 检查是否有新文件
    new_files = current_files - last_files
    if new_files:
        print("发现新文件")
        for file in new_files:
            q = whisper2text(file)
            a = robotChat(q)
            robot_speak(a, file)
        # 更新last_files为当前文件集合
        last_files = current_files

def whisper2text(file_name):
    absolute_path = os.path.abspath(os.path.join(monitor_directory, file_name))
    print(f"using whisper processing the file: {absolute_path}")
    result = model.transcribe(absolute_path, fp16=False)

    content = result["text"]

    print(content)

    return content

def robotChat(prompt):
    response = ollama.generate(model=llm_model, prompt=prompt)
    answer = response['response']
    print(answer)

    return answer

def robot_speak(content, ask_file_name):
    # speak_pytts(content)
    speak_ChatTTS(content, ask_file_name)


def speak_pytts(content):
    # rate = engine.getProperty('rate')   
    volume = engine.getProperty('volume')
    engine.setProperty('rate', 120)  # 语速
    engine.setProperty('volume', volume + 0.25)  # 音量
    # engine.setProperty('voice', 'com.apple.voice.compact.zh-TW.Meijia') #台湾
    engine.setProperty('voice', 'com.apple.voice.compact.zh-CN.Tingting') #大陆
    # engine.setProperty('voice', 'com.apple.voice.compact.zh-HK.Sinji') #粤语

    engine.say(content)
    engine.runAndWait()

def speak_ChatTTS(content, ask_file_name):
    chat = ChatTTS.Chat()
    chat.load(compile=False)
    wavs = chat.infer([content])

    for i in range(len(wavs)):
        reply_file_name = f"{chat_reply_directory}/reply{i}_{ask_file_name}"
        torchaudio.save(reply_file_name, torch.from_numpy(wavs[i]), 24000)
        play_wav(reply_file_name)
    
def play_wav(file_path):
    print(file_path)
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()

# 启动服务循环
counter = 0
try:
    while True:
        counter = counter + 1
        print(f"第{counter}轮，监听收否有人和我说话……")
        check_new_files(monitor_directory)
        time.sleep(5)  # 等待5秒
except KeyboardInterrupt:
    print("服务已停止。")