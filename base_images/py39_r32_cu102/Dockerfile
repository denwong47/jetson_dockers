FROM nvcr.io/nvidia/l4t-base:r32.7.1

ARG PYTHON_VERSION="3.9.16"

RUN apt update && apt install -y git htop curl wget nano 

RUN apt install -y \
	build-essential \
	libncursesw5-dev \
	libreadline-dev \
	libssl-dev \
	libgdbm-dev \
	libc6-dev \
	libsqlite3-dev \
	libbz2-dev \
	libffi-dev \
    zlib1g-dev \
    openssl

WORKDIR /root/Downloads
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz
RUN tar -zxvf Python-${PYTHON_VERSION}.tgz
RUN rm -rf PYTHON-${PYTHON_VERSION}.tgz

WORKDIR /root/Downloads/Python-${PYTHON_VERSION}
RUN ./configure --enable-optimizations --enable-loadable-sqlite-extensions --with-ssl
COPY ./modules_setup_ssl.local ./
RUN cat ./modules_setup_ssl.local >> ./Modules/Setup.local
RUN rm ./modules_setup_ssl.local
RUN ls -la /usr/include/openssl
RUN make altinstall

WORKDIR /root/Downloads
RUN rm -rf Python-${PYTHON_VERSION}

RUN python3.9 -m pip install --upgrade pip ipython pytest setuptools wheel

COPY ./fake-nvidia-smi.py /var/fake-nvidia-smi/
RUN ln -s fake-nvidia-smi.py /var/fake-nvidia-smi/nvidia-smi
ENV PATH="/var/fake-nvidia-smi:${PATH}"