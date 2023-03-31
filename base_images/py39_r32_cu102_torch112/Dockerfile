FROM py39_r32_cu102

# Install pre-built wheel of pytorch; see builder_images/build_cu102/pytorch112
COPY ./wheels .
RUN python3.9 -m pip install ./wheels/torch-1.12.0a0+git045657b-cp39-cp39-linux_aarch64.whl
