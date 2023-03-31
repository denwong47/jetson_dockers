FROM py39_r32_cu102_torch112

ARG TS_VERSION=0.6.0

# This Dockerfile is a heavily trimmed down version of the
# [AWS Recipe for PyTorch Inference](https://github.com/aws/deep-learning-containers/blob/master/pytorch/inference/docker/1.11/py3/cu113/Dockerfile.gpu).

WORKDIR /root
COPY ./requirements.txt .
RUN python3.9 -m pip install -r requirements.txt
RUN rm ./requirements.txtexit

RUN pip install --no-cache-dir -U \
    "awscli<2" \
    boto3 \
    "cryptography>3.2" \
    enum-compat==0.0.3 \
    "ipython>=8.10,<9" \
    numpy==1.22.2 \
    "opencv-python>=4.6,<5" \
    packaging \
    "pyyaml>=5.4,<5.5"

# Install Java
RUN apt install default-jre
RUN pip uninstall -y model-archiver multi-model-server \
 && pip install torchserve==${TS_VERSION} \
 && pip install torch-model-archiver==${TS_VERSION}

# Install TorchServe pypi dependencies directly from their requirements.txt file
RUN pip install --no-cache-dir -U -r https://raw.githubusercontent.com/pytorch/serve/v${TS_VERSION}/requirements/common.txt

# Pillow is pinned in TS 0.6.0 to an obsolete version. To work around this, re-install in a separate line
RUN pip install --no-cache-dir -U "Pillow>=9.3.0,<10"

WORKDIR /

# System setup
RUN cd tmp/ \
 && rm -rf tmp*

RUN useradd -m model-server \
 && mkdir -p /home/model-server/tmp /opt/ml/model \
 && chown -R model-server /home/model-server /opt/ml/model

COPY config.properties /home/model-server

COPY torchserve-sagemaker-entrypoint.py /usr/local/bin/dockerd-entrypoint.py
COPY deep_learning_container.py /usr/local/bin/deep_learning_container.py

RUN chmod +x /usr/local/bin/dockerd-entrypoint.py
RUN chmod +x /usr/local/bin/deep_learning_container.py

RUN pip install --no-cache-dir sagemaker-pytorch-inference sagemaker-inference

EXPOSE 8080 8081

ENTRYPOINT ["python3.9", "/usr/local/bin/dockerd-entrypoint.py"]
CMD ["torchserve", "--start", "--ts-config", "/home/model-server/config.properties", "--model-store", "/home/model-server/"]