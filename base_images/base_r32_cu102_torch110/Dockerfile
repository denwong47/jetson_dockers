FROM nvcr.io/nvidia/l4t-pytorch:r32.7.1-pth1.10-py3

# Not sure what this repo is, but it is missing its GPG key.
RUN add-apt-repository --remove "deb https://apt.kitware.com/ubuntu/ bionic main"
RUN apt update && apt install -y git htop curl wget nano 
RUN python3 -m pip install --upgrade pip ipython pytest
