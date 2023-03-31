FROM py39_r32_cu102

# Builds a specific AArch64 PyTorch with CUDA from source.
# This is not a standard wheel they pre-build.

# This file is entirely based on an article by Q-engineering:
# https://qengineering.eu/install-pytorch-on-jetson-nano.html

RUN apt install -y \
    ninja-build \
    git \
    cmake \
    libjpeg-dev \
    libopenmpi-dev \
    libomp-dev \
    ccache \
    libopenblas-dev \
    libblas-dev \
    libeigen3-dev \
    clang-8

RUN python3.9 -m pip install -U --user wheel mock pillow
RUN python3.9 -m pip install testresources setuptools==58.3.0 scikit-build
RUN ln -s /usr/bin/clang-8 /usr/bin/clang
RUN ln -s /usr/bin/clang++-8 /usr/bin/clang++

WORKDIR /root/Downloads
RUN git clone -b v1.12.1-aarch64-cuda --depth=1 --recursive https://github.com/denwong47/pytorch.git

WORKDIR /root/Downloads/pytorch
RUN python3.9 -m pip install -r requirements.txt

ENV BUILD_CAFFE2_OPS=OFF
ENV USE_FBGEMM=OFF
ENV USE_FAKELOWP=OFF
ENV BUILD_TEST=OFF
ENV USE_MKLDNN=OFF
ENV USE_NNPACK=OFF
ENV USE_XNNPACK=OFF
ENV USE_QNNPACK=OFF
ENV USE_PYTORCH_QNNPACK=OFF
ENV USE_CUDA=ON
ENV USE_CUDNN=ON
ENV TORCH_CUDA_ARCH_LIST="5.3;6.2;7.2"
ENV USE_NCCL=OFF
ENV USE_SYSTEM_NCCL=OFF
ENV USE_OPENCV=OFF
ENV MAX_JOBS=4
# set path to ccache
ENV PATH=/usr/lib/ccache:$PATH
# set clang compiler
ENV CC=clang
ENV CXX=clang++
# set cuda compiler
ENV CUDACXX=/usr/local/cuda/bin/nvcc

RUN ln -s /usr/lib/aarch64-linux-gnu/libcublas.so /usr/local/cuda/lib64/libcublas.so
RUN mkdir ./wheels

COPY ./cmake/bin/* /usr/bin/
COPY ./cmake/share/cmake-3.26 /usr/share/cmake-3.26
ENTRYPOINT [ "python3.9", "setup.py", "bdist_wheel" ]