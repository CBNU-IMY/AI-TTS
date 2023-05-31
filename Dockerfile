#FROM ubuntu:18.04\pytorch\pytorch:1.7.1-cuda11.0-cudnn8-devel
FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-devel

RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    unzip \
    git \
    espeak-ng \
    libsndfile1-dev \

 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    "konlpy" \ 
    "jamo" \ 
    "nltk" \
    "numpy" \
    "python-mecab-ko" \
    "onnxruntime" \
    "flask"

RUN mkdir -p /content/src

WORKDIR /content/src

RUN git clone --depth 1 https://github.com/sce-tts/g2pK.git
RUN git clone --depth 1 https://github.com/sce-tts/TTS.git -b sce-tts

WORKDIR /content/src/g2pK
RUN pip install --no-cache-dir -e .

WORKDIR /content/src/TTS
RUN pip install --no-cache-dir -e .

RUN pip install numpy==1.23.0 --ignore-installed
RUN pip install resampy==0.3.1
RUN pip install spacy
#RUN pip uninstall -y ipython prompt_toolki
#RUN pip install -ipython prompt_toolkit

RUN mkdir -p /content/src/flask
WORKDIR /content/src/flask
EXPOSE 5001

CMD ["python","-u", "server.py"]