import os
import time
import whisper
import ollama
import pyttsx3

# 指定要监控的目录
monitor_directory = "./records"  # 修改为你的目录路径

# 初始化上一次检查的文件集合
last_files = set(os.listdir(monitor_directory))

# Initialize Whisper model in CPU mode
model = whisper.load_model("base", device="cpu")
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
            robot_speak(a)
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
    response = ollama.generate(model='llama3', prompt=prompt)
    answer = response['response']
    print(answer)

    return answer

def robot_speak(content):
    # rate = engine.getProperty('rate')   
    volume = engine.getProperty('volume')
    engine.setProperty('rate', 120)  # 语速
    engine.setProperty('volume', volume + 0.25)  # 音量
    engine.setProperty('voice', 'com.apple.voice.compact.zh-TW.Meijia') #台湾
    # engine.setProperty('voice', 'com.apple.voice.compact.zh-CN.Tingting') #大陆
    # engine.setProperty('voice', 'com.apple.voice.compact.zh-HK.Sinji') #粤语

    engine.say(content)
    engine.runAndWait()


# 启动服务循环
try:
    while True:
        check_new_files(monitor_directory)
        time.sleep(5)  # 等待5秒
except KeyboardInterrupt:
    print("服务已停止。")