# 运行 cuda 容器显示未检测到驱动

## 问题

以镜像 `nvidia/cuda:12.8.1-devel-ubuntu22.04` 为例：

```console
$ docker run -it --rm nvidia/cuda:12.8.1-devel-ubuntu22.04

==========
== CUDA ==
==========

CUDA Version 12.8.1

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.

WARNING: The NVIDIA Driver was not detected.  GPU functionality will not be available.
   Use the NVIDIA Container Toolkit to start this container with GPU support; see
   https://docs.nvidia.com/datacenter/cloud-native/ .
```

这种情况下 Nvidia 管理工具和 CUDA 动态链接库也都不存在：

```console
# ls /usr/bin/nvidia-smi /lib/x86_64-linux-gnu/libcuda.so.1 
ls: cannot access '/usr/bin/nvidia-smi': No such file or directory
ls: cannot access '/lib/x86_64-linux-gnu/libcuda.so.1': No such file or directory
```

## 原因

在 <https://hub.docker.com/> 查看镜像 Layers, 可以看到镜像入口

```docker
ENTRYPOINT ["/opt/nvidia/nvidia_entrypoint.sh"]
```

在容器中查看文件 `/opt/nvidia/nvidia_entrypoint.sh` 发现其引用了目录 `/opt/nvidia/entrypoint.d` 下的所有脚本，其中有一个文件 `50-gpu-driver-check.sh`:

```sh
#!/bin/bash
# Copyright (c) 2017-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

# Check if libcuda.so.1 -- the CUDA driver -- is present in the ld.so cache or in LD_LIBRARY_PATH
_LIBCUDA_FROM_LD_CACHE=$(ldconfig -p | grep libcuda.so.1)
_LIBCUDA_FROM_LD_LIBRARY_PATH=$( ( IFS=: ; for i in ${LD_LIBRARY_PATH}; do ls $i/libcuda.so.1 2>/dev/null | grep -v compat; done) )
_LIBCUDA_FOUND="${_LIBCUDA_FROM_LD_CACHE}${_LIBCUDA_FROM_LD_LIBRARY_PATH}"

# Check if /dev/nvidiactl (like on Linux) or /dev/dxg (like on WSL2) or /dev/nvgpu (like on Tegra) is present
_DRIVER_FOUND=$(ls /dev/nvidiactl /dev/dxg /dev/nvgpu 2>/dev/null)

# If either is not true, then GPU functionality won't be usable.
if [[ -z "${_LIBCUDA_FOUND}" || -z "${_DRIVER_FOUND}" ]]; then
  echo
  echo "WARNING: The NVIDIA Driver was not detected.  GPU functionality will not be available."
  echo "   Use the NVIDIA Container Toolkit to start this container with GPU support; see"
  echo "   https://docs.nvidia.com/datacenter/cloud-native/ ."
  export NVIDIA_CPU_ONLY=1
fi
```

可以看到此脚本实际是检测以下三个设备文件是否存在：

- `/dev/nvidiactl`
- `/dev/dxg`
- `/dev/nvgpu`

其中后两个设备甚至在主机上也不存在。

## 解决方案

解决方案正如提示信息中所说，安装 `nvidia-container-toolkit`.

首先配置 nvidia 源：

```console
$ curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
$ curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

安装：

```console
$ sudo apt update
$ sudo apt install -y nvidia-container-toolkit
```

配置 docker:

```console
$ sudo nvidia-ctk runtime configure --runtime=docker
INFO[0000] Loading config from /etc/docker/daemon.json  
INFO[0000] Wrote updated config to /etc/docker/daemon.json 
INFO[0000] It is recommended that docker daemon be restarted.
```

实际上在 `/etc/docker/daemon.json` 中增加了以下内容：

```diff
<     ]
---
>     ],
>     "runtimes": {
>         "nvidia": {
>             "args": [],
>             "path": "nvidia-container-runtime"
>         }
>     }
```

重启 docker 使之生效：

```console
$ sudo systemctl restart docker
```

:::{tip}
实际上 `runtimes` 配置并非必须，只是可以允许用 `--runtime` 参数运行其他非 cuda 映像，如：

```console
$ sudo docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

:::

再次运行镜像，并添加 `--gpus all` 参数会发现错误信息消失了：

```console
$ docker run -it --rm --gpus all nvidia/cuda:12.8.1-devel-ubuntu22.04

==========
== CUDA ==
==========

CUDA Version 12.8.1

Container image Copyright (c) 2016-2023, NVIDIA CORPORATION & AFFILIATES. All rights reserved.

This container image and its contents are governed by the NVIDIA Deep Learning Container License.
By pulling and using the container, you accept the terms and conditions of this license:
https://developer.nvidia.com/ngc/nvidia-deep-learning-container-license

A copy of this license is made available in this container at /NGC-DL-CONTAINER-LICENSE for your convenience.
```

这时在镜像中查看设备文件，会发现 `/dev/dxg` 和 `/dev/nvgpu` 仍然不存在，也就是说它们仅服务于容器初始化目的：

```console
# ls /dev/nvidiactl /dev/dxg /dev/nvgpu
ls: cannot access '/dev/dxg': No such file or directory
ls: cannot access '/dev/nvgpu': No such file or directory
/dev/nvidiactl
```

查看 `nvidia-smi` 和 `libcuda.so.1`

```console
# which nvidia-smi
/usr/bin/nvidia-smi
# ls -l /lib/x86_64-linux-gnu/libcuda.so.1 
lrwxrwxrwx 1 root root 20 Apr 10 05:54 /lib/x86_64-linux-gnu/libcuda.so.1 -> libcuda.so.560.35.05
```
