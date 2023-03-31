# Base image for PyTorch 1.12 on CUDA 10.2 with Python 3.9

Use
```sh
make build
make run
```

This image requires `wheels` from `builder_images/build_cu102_pytorch112` to be
manually copied over to build successfully.

A pre-built wheel is also available on [GitHub](https://github.com/denwong47/pytorch/releases/tag/v1.12.1%2Bcu102_aarch64).