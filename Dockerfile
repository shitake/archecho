FROM ubuntu:20.04

ENV PYTHON_VERSION=3.8
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        cmake \
        curl \
        file \
        g++ \
        gcc \
        git \
        libmecab-dev \
        mecab \
        mecab-ipadic-utf8 \
        software-properties-common \
        sudo \
        swig \
        vim \
        xz-utils \
        zip \
    && rm -rf /var/lib/apt/lists/*

# NEologd
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /tmp/neologd \
    && /tmp/neologd/bin/install-mecab-ipadic-neologd -n -y \
    && rm -rf /tmp/neologd

# Locale
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install -y \
        language-pack-ja-base \
        language-pack-ja
RUN update-locale LANG=ja_JP.UTF-8

# Install Python
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python${PYTHON_VERSION} \
    && apt-get install python3-pip python3-venv -y
RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python3 \
    && ln -s /usr/bin/python${PYTHON_VERSION} /usr/local/bin/python \
    && ln -s /usr/bin/pip3 /usr/local/bin/pip \
    && pip install --upgrade pip

# Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH /root/.poetry/bin:$PATH
RUN poetry completions bash > /etc/bash_completion.d/poetry.bash-completion \
    && poetry self update \
    && poetry config virtualenvs.in-project true --local

WORKDIR /home/archecho

# Config and clean up
RUN ldconfig \
    && apt-get clean \
    && apt-get autoremove

