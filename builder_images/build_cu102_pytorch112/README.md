# Builder for PyTorch 1.12 on CUDA 10.2 with Python 3.9

Use
```sh
make build
make run
```

Upon running this, the image will build the wheels for PyTorch, outputting to the
directory of `wheels`.

Some base images such as `py39_r32_cu102_torch112` requires these `wheels` to be
manually copied over to build successfully.