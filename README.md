**Dockerfiles** for building
# Container images for NVidia Jetson Nano SBC

This repo contains various `Dockerfile`s derived from NVidia's official `L4T` ones,
for the purpose of upgrading and installing

- newer Python versions
- newer PyTorch versions etc.

We cannot easily upgrade CUDA itself for outdated Jetson Nanos. For P3450 for example,
it can only use Jetpack <= 4.6.3. which came with CUDA 10.2 on Ubuntu 18.04. The
official PyTorch image for this device came with Python 3.6 and Pytorch 1.10, making
a lot of modern libraries incompatible. Backporting those libraries are almost
an impossibly difficult task due to typing changes, as well as lesser problems such as
the `:=` operator.

This repo builds a newer Python vesion from source, alongside but not replacing the
system Python. Then it uses the new Python to `pip install` newer versions of packages
where available.

Typically packages do not pre-build wheels for CUDA on AArch64 as its an incredibly
niche use case, so this repo builds those from source where required as well
(eg. PyTorch).

The build process can take hours and can require a lot of swap disk space.
