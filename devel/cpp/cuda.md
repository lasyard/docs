# CUDA

<https://developer.nvidia.com/cuda-toolkit>

Download the installer:

```console
$ curl -LO https://developer.download.nvidia.com/compute/cuda/12.6.3/local_installers/cuda_12.6.3_560.35.05_linux.run
```

Run the installer:

```console
$ chmod +x cuda_12.6.3_560.35.05_linux.run
$ sudo ./cuda_12.6.3_560.35.05_linux.run
```

:::{note}
Be patient! It is slow and need interactive inputs.
:::

Show version:

```console
$ /usr/local/cuda-12.6/bin/nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2024 NVIDIA Corporation
Built on Tue_Oct_29_23:50:19_PDT_2024
Cuda compilation tools, release 12.6, V12.6.85
Build cuda_12.6.r12.6/compiler.35059454_0
```
