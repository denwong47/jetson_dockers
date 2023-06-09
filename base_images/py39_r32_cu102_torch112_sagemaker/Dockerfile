FROM py39_r32_cu102_torch112

ARG TS_VERSION=0.6.0
ARG PIP_INSTALL='python3.9 -m pip install'
ARG DEPENDENCY_DIR='.dependencies'
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

ENV PATH="/opt/ml/model/code:${PATH}"

# Defines inference_code.py as script entrypoint
ENV SAGEMAKER_SUBMIT_DIRECTORY /opt/ml/model/code
ENV SAGEMAKER_PROGRAM inference_code.py
ENV SAGEMAKER_CONTAINER_LOG_LEVEL 20
ENV SAGEMAKER_ENABLE_CLOUDWATCH_METRICS False
ENV SAGEMAKER_REGION eu-west-2
ENV SAGEMAKER_BIND_TO_PORT 8080
ENV SAGEMAKER_MODEL_SERVER_TIMEOUT 3600
ENV SAGEMAKER_RESPONSE_TIMEOUT 120

ENV AWS_DEFAULT_REGION ${SAGEMAKER_REGION}
ENV AWS_REGION ${SAGEMAKER_REGION}
ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}


# This Dockerfile is a heavily trimmed down version of the
# [AWS Recipe for PyTorch Inference](https://github.com/aws/deep-learning-containers/blob/master/pytorch/inference/docker/1.11/py3/cu113/Dockerfile.gpu).

WORKDIR /root
COPY ./requirements.txt .
RUN ${PIP_INSTALL} -r requirements.txt
RUN rm ./requirements.txt

RUN ${PIP_INSTALL} --no-cache-dir -U \
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
RUN apt install -y default-jre
RUN ${PIP_INSTALL} torchserve==${TS_VERSION} \
 && ${PIP_INSTALL} torch-model-archiver==${TS_VERSION}

# Install TorchServe pypi dependencies directly from their requirements.txt file
RUN ${PIP_INSTALL} --no-cache-dir -U -r https://raw.githubusercontent.com/pytorch/serve/v${TS_VERSION}/requirements/common.txt

# Pillow is pinned in TS 0.6.0 to an obsolete version. To work around this, re-install in a separate line
RUN ${PIP_INSTALL} --no-cache-dir -U "Pillow>=9.3.0,<10"

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

RUN ${PIP_INSTALL} --no-cache-dir sagemaker-pytorch-inference sagemaker-inference

RUN ${PIP_INSTALL} "cupy-cuda102<12.0.0,>=5.0.0b4"
RUN ${PIP_INSTALL} spacy[cu102] spacy_fastlang textblob GPUtil openpyxl

# # CUDA packages
# RUN ${PIP_INSTALL} cudf-cuda100 --extra-index-url=https://pypi.nvidia.com
# RUN ${PIP_INSTALL} cuml-cuda100 --extra-index-url=https://pypi.nvidia.com
# RUN ${PIP_INSTALL} cugraph-cuda100 --extra-index-url=https://pypi.nvidia.com

EXPOSE 8080 8081

ENTRYPOINT ["python3.9", "/usr/local/bin/dockerd-entrypoint.py"]
CMD ["torchserve", "--start", "--ts-config", "/home/model-server/config.properties", "--model-store", "/home/model-server/"]