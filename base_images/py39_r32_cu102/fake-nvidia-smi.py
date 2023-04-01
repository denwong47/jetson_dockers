#!/usr/bin/env python3
import argparse
from datetime import datetime
import uuid

CUDA_VERSION="10.2"
DRIVER_VERSION="440.296.70" # 440 is correct but everything behind is random
SMI_VERSION=DRIVER_VERSION

# Pre-generate this to make it consistent
GPU_UUID = uuid.uuid4()

LIST_FORMATTER: str = "GPU 0: NVIDIA Tegra X1 (UUID: GPU-{uuid})"
INDEX_FORMATER: str = "index\n0"
TABLE_FORMATTER: str = (
"""{now:%a %b %2d %H:%M:%S %Y}
+-----------------------------------------------------------------------------+
| NVIDIA-SMI {smi_version:13}Driver Version: {driver_version:13}CUDA Version: {cuda_version:9}|
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA Tegra ...    On   | 00000000:01:00.0 Off |                  N/A |
|  0%   34C    P8    N/A / 120W |      1MiB /  4040MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
"""
)

# References:
# - https://github.com/pytorch/serve/issues/1289
# - https://github.com/rossumai/nvgpu/blob/master/nvgpu/__init__.py#L14

parser = argparse.ArgumentParser(
                    prog='Fake nVidia SMI',
                    description=(
                        'Fake NVIDIA System Management Interface. '
                        'Jetson Nano boards cannot use the standard '
                        '`nvidia-smi` utilities, but a lot of Python '
                        'utilities such as `torchserve` and '
                        '`nvgpu` depends on parsing the output of '
                        '`nvidia-smi` to check GPU capabilities. '
                        'This utilities create a fake `nvidia-smi` '
                        'stdout so that these utilities can parse it.'
                    ),
)

parser.add_argument('--query_gpu', metavar="column", type=str,
                    help=(
                        'Information about GPU. Currently only index '
                        'is supported.'
                    ))
parser.add_argument('-L', '--list-gpus',
                    action='store_true',
                    dest="list_gpus",
                    help='Display a list of GPUs connected to the system.')
parser.add_argument('--format',
                    type=str,
                    help=(
                        "Comma separated list of format options:\n"
                        "       csv - comma separated values (MANDATORY)\n"
                        "       noheader - skip the first line with column headers\n"
                        "       nounits - don't print units for numerical values"
                    ))

if __name__=="__main__":
    args = parser.parse_args()

    _query_gpu = args.query_gpu and args.query_gpu.split(",")
    _list_gpus = args.list_gpus
    _format = args.format and args.format.split(",")

    if _list_gpus:
        print(
            LIST_FORMATTER.format(uuid=GPU_UUID)
        )
    elif _query_gpu:
        if _format != ["csv"]:
            raise ValueError(
                "Only csv is supported for format."
            )
        
        if _query_gpu != ["index"]:
            raise ValueError(
                "Only index is supported for query_gpu."
            )
        
        print(
            INDEX_FORMATER
        )
    else:
        print(
            TABLE_FORMATTER.format(
                now=datetime.now(),
                smi_version=SMI_VERSION,
                driver_version=DRIVER_VERSION,
                cuda_version=CUDA_VERSION,
            )
        )