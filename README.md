# chat_robot
from audio to audio answer from AI LLM

## install

### 1. install client audio record
```
sudo apt install portaudio19-dev python-all-dev python3-all-dev

pip isntall pyaudio

```

- trouble shooting:

libstdc++.so.6: version `GLIBCXX_3.4.32' not found (required by /lib/x86_64-linux-gnu/libjack.so.0)

```
sudo add-apt-repository ppa:ubuntu-toolchain-r/test
sudo apt update
sudo apt install --only-upgrade libstdc++6
#check if you get GLIBCXX desired version like this:
strings /usr/lib/x86_64-linux-gnu/libstdc++.so.6 | grep GLIBCXX


ln -sf /usr/lib/x86_64-linux-gnu/libstdc++.so.6 /home/terry/anaconda3/envs/chat_robot/lib/libstdc++.so.6
```

### 2. install whisper
```
sudo apt update && sudo apt install ffmpeg

pip install -U openai-whisper
```

### 3. install local LLM
- install ollama

    - install docker
    ```
    sudo apt  install docker.io
    ```

- Install the NVIDIA Container Toolkit⁠
    - Configure the repository
    ```
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
        | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
        | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
        | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
    sudo apt-get update

    ```

    - Install the NVIDIA Container Toolkit packages

    ```
    sudo apt install -y nvidia-container-toolkit

    ```

    - Configure Docker to use Nvidia driver
    ```
    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker

    ```

```
sudo docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# install llama3
sudo docker exec -it ollama ollama run llama3

# install llama3.1
sudo docker exec -it ollama ollama run llama3.1

```
- troble shooting

    if the ollama docker image can not be pulled, change the repositry mirro

    - edit /etc/docker/daemon.json
    ```
    sudo vim /etc/docker/daemon.json
    ```
    input: <br/>
    {"registry-mirrors": ["https://do.nark.eu.org/"]}

    ```
    systemctl daemon-reload
    systemctl restart docker

    #check change success or not
    sudo docker info
    ```
- install ollama-python
```
pip install ollama
```


### 4. install TTS
- pyttsx3
```
pip install pyttsx3
```

- ChatTTS
```
pip install ChatTTS
```

- trouble shooting

    - OSError: libespeak.so.1: cannot open shared object file: No such file or directory

    ```
    sudo apt install espeak

    ```


    - raise RuntimeError(f"Couldn't find appropriate backend to handle uri {uri} and format {format}."

    ```
    pip install soundfile

    ```

    - raise Error('unknown format: %r' % (wFormatTag,)) wave.Error: unknown format: 3

    ```
    pip install sounddevice

    ```

### others
install audio player on ubuntu
```
sudo apt install sox libsox-fmt-all

play *.mp3
play *.wav
```