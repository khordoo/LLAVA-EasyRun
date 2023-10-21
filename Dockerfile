#FROM python:3.10-buster
#RUN apt-get update \
#    && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends build-essential \
#    && rm -rf /var/lib/apt/lists/*
#WORKDIR /app
#RUN git clone https://github.com/ggerganov/llama.cpp.git /app
#RUN pip install -r requirements.txt
#RUN make llava
#RUN ls /app
#CMD ["sleep","50000"]
# Dockerfile to deploy a llama-cpp container with conda-ready environments

# docker pull continuumio/miniconda3:latest

ARG TAG=latest
FROM continuumio/miniconda3:$TAG

RUN apt-get update \
    && DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        git \
        locales \
        sudo \
        build-essential \
        dpkg-dev \
        wget \
        openssh-server \
        nano \
    && rm -rf /var/lib/apt/lists/*

# Setting up locales

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8

# SSH exposition

EXPOSE 22/tcp
RUN service ssh start

# Create user

RUN groupadd --gid 1020 llama-cpp-group
RUN useradd -rm -d /home/llama-cpp-user -s /bin/bash -G users,sudo,llama-cpp-group -u 1000 llama-cpp-user

# Update user password
RUN echo 'llama-cpp-user:admin' | chpasswd

# Updating conda to the latest version
RUN conda update conda -y

# Create virtalenv
RUN conda create -n llamacpp -y python=3.10.6

# Adding ownership of /opt/conda to $user
RUN chown -R llama-cpp-user:users /opt/conda

# conda init bash for $user
RUN su - llama-cpp-user -c "conda init bash"

# Download latest github/llama-cpp in llama.cpp directory and compile it
RUN su - llama-cpp-user -c "git clone https://github.com/ggerganov/llama.cpp.git ~/llama.cpp \
                            && cd ~/llama.cpp \
                            && make llava"

# Install Requirements for python virtualenv
RUN su - llama-cpp-user -c "cd ~/llama.cpp \
                            && conda activate llamacpp \
                            && python3 -m pip install -r requirements.txt "

# Download model
RUN su - llama-cpp-user -c "cd ~/llama.cpp/models \
                            && wget https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/ggml-model-q4_k.gguf \
                            && wget https://huggingface.co/mys/ggml_llava-v1.5-7b/resolve/main/mmproj-model-f16.gguf "


# Install Requirements for Streamlit GUI Depedencies
RUN su - llama-cpp-user -c "cd ~/llama.cpp \
                            && conda activate llamacpp \
                            && python3 -m pip install streamlit==1.27.2 watchdog==3.0.0 "

# Copy GUI Streamlit application
WORKDIR /home/llama-cpp-user/llama.cpp
COPY app.py .
EXPOSE 8501

# Preparing for login
ENV HOME /home/llama-cpp-user
WORKDIR ${HOME}/llama.cpp
USER llama-cpp-user
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "llamacpp", "streamlit","run", "app.py"]

#CMD ["sleep","5000"]
